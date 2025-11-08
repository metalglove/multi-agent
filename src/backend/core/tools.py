import os
import time
from typing import List, Dict, Any, Optional
import json
import ast
import re
import base64

from crewai.tools.base_tool import BaseTool


class BatchFileWriterTool(BaseTool):
	"""A CrewAI-compatible tool that accepts a list of file dicts and writes
	them one-by-one using an underlying FileWriterTool instance.

	This class subclasses `BaseTool` so it can be added to an Agent's
	`tools` list and validated by the crewai model.
	"""

	# Use a human-friendly tool name so prompts don't need to repeat a
	# machine-oriented identifier. The runtime will still register the
	# tool object and the agents will receive this display name.
	name: str = "Batch File Writer Tool"
	description: str = "Write multiple files by delegating to the FileWriterTool"

	_writer: Any = None
	default_directory: Optional[str] = None
	max_retries: int = 3

	def __init__(self, writer=None, default_directory: Optional[str] = None, max_retries: int = 3, **data):
		super().__init__(**data)
		self._writer = writer
		self.default_directory = default_directory
		self.max_retries = max_retries

	def _write_single(self, payload: Dict[str, Any]) -> Dict[str, Any]:
		filename = payload.get("filename")
		# Support multiple content encodings to make agents' lives easier. Preferred order:
		# 1. content_b64: base64-encoded bytes of the content (recommended for large or quote-heavy text)
		# 2. content with content_encoding == 'base64'
		# 3. plain content string
		content = None
		if "content_b64" in payload:
			try:
				content = base64.b64decode(payload["content_b64"]).decode("utf-8")
			except Exception as e:
				return {"filename": filename, "success": False, "path": None, "error": f"Invalid base64 content: {e}"}
		elif payload.get("content_encoding") == "base64" and payload.get("content"):
			try:
				content = base64.b64decode(payload["content"]).decode("utf-8")
			except Exception as e:
				return {"filename": filename, "success": False, "path": None, "error": f"Invalid base64 content: {e}"}
		else:
			content = payload.get("content")
		if filename is None or content is None:
			return {"filename": filename, "success": False, "path": None, "error": "Missing filename or content"}

		directory = payload.get("directory") or self.default_directory

		# Accept the human-friendly placeholder used in task prompts
		# ('<directory>') and substitute it with the configured
		# default_directory. This prevents agents from accidentally
		# passing the literal placeholder string as a filesystem path
		# which causes OS errors (seen on Windows as WinError 123).
		if isinstance(directory, str) and directory.strip() in ("<directory>", "<output_directory>", "<output>"):
			directory = self.default_directory
		# If we still don't have a directory, fail early with a clear error
		if directory is None:
			return {"filename": filename, "success": False, "path": None, "error": "No target directory provided; set 'directory' or configure default_directory for the tool."}
		requested_overwrite = payload.get("overwrite", None)

		# Prepare kwargs for the underlying writer. Pass directory and overwrite
		# explicitly so that FileWriterTool._run can see them and create the
		# target directory before attempting to write.
		single = {"filename": filename, "content": content}
		if directory:
			single["directory"] = directory
		# Ensure an overwrite key is always present so the underlying
		# FileWriterTool can safely read it. If caller didn't provide an
		# explicit value, default to False.
		single["overwrite"] = requested_overwrite if requested_overwrite is not None else False

		attempt = 0
		last_error = None
		while attempt <= self.max_retries:
			try:
				# The FileWriterTool provides a `run` method; call it directly.
				# This keeps the behavior simple and matches the tool in
				# site-packages/crewai_tools.
				result = self._writer.run(**single)

				# Normalize reported path to an absolute path for clarity.
				if directory:
					written_path = os.path.abspath(os.path.join(directory, filename))
				else:
					written_path = os.path.abspath(filename)
				warning = None
				returned_result = result

				# The wrapped FileWriterTool returns human-readable strings. Try to
				# detect common cases and surface them in structured fields.
				if isinstance(result, str):
					low = result.lower()
					# If the underlying writer mentions 'overwrite' or 'already exists'
					# treat that as a warning (not fatal) unless caller requested
					# overwrite explicitly.
					if "overwrite" in low or "already exists" in low:
						warning = result
						# leave returned_result as the original string so callers can
						# inspect it if needed.

				# If caller requested overwrite, but the underlying writer didn't
				# report anything, add a gentle note so users understand the
				# writer was instantiated with overwrite enabled.
				if requested_overwrite and warning is None:
					warning = "Caller requested overwrite; file_write_tool_initialized with allow_overwrite=True"

				return {"filename": filename, "success": True, "path": written_path, "error": None, "result": returned_result, "warning": warning}
			except Exception as e:
				last_error = str(e)
				attempt += 1
				# Prefer non-blocking asyncio sleep when running outside an
				# active event loop; if an event loop is already running we
				# cannot await here in this synchronous function, so fall
				# back to a short blocking sleep. This keeps the retry
				# behavior safe for both sync and async call sites. If you
				# want fully non-blocking retries, we should add async
				# versions of these methods.
				try:
					import asyncio
					loop = asyncio.get_running_loop()
					# If we're here, an event loop is running; avoid trying to
					# schedule awaits from sync code — use blocking sleep.
					time.sleep(0.2 * attempt)
				except RuntimeError:
					# No running loop — use asyncio.run to perform a non-blocking
					# sleep (this will block the thread briefly while running
					# the coroutine, but avoids importing asyncio.sleep into
					# already-running loops).
					import asyncio
					asyncio.run(asyncio.sleep(0.2 * attempt))
		return {"filename": filename, "success": False, "path": None, "error": last_error}

	def run(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		# Accept either an already-deserialized list, or a string that contains
		# a JSON array. Models sometimes return the JSON array as text; try to
		# extract and parse it robustly.
		if isinstance(files, str):
			# Try to find the first JSON array substring in the string.
			m = re.search(r"(\[.*\])", files, flags=re.DOTALL)
			if m:
				candidate = m.group(1)
				try:
					files = json.loads(candidate)
				except Exception:
					# Fallback to python literal eval which accepts single quotes etc.
					try:
						files = ast.literal_eval(candidate)
					except Exception:
						raise ValueError(
							"BatchFileWriterTool could not parse the provided string as a JSON/Python list. "
							"Ask the agent to return a JSON array or encode content as base64 (see task instructions)."
					)
			else:
				raise ValueError("BatchFileWriterTool expects a list of file dicts or a string containing a JSON array.")
		if not isinstance(files, list):
			raise ValueError("BatchFileWriterTool expects a list of file dicts.")

		# Validate each item early and provide a clear error if the caller
		# passed an unexpected type (common when an LLM or prompt-produced
		# payload accidentally produces a list of strings instead of a list
		# of dicts). Raising a descriptive TypeError makes debugging much
		# faster than letting downstream code fail with obscure messages.
		for idx, item in enumerate(files):
			# If model returned items as strings, attempt to parse each element.
			if not isinstance(item, dict):
				if isinstance(item, str):
					# Try to parse JSON or python literal for this item
					try:
						parsed = json.loads(item)
					except Exception:
						try:
							parsed = ast.literal_eval(item)
						except Exception:
							raise TypeError(
								f"BatchFileWriterTool: could not parse files[{idx}] string into a dict."
						)
					if not isinstance(parsed, dict):
						raise TypeError(
							f"BatchFileWriterTool: expected dict for files[{idx}] after parsing, got {type(parsed).__name__}."
					)
					item = parsed
				else:
					raise TypeError(
						f"BatchFileWriterTool: expected dict for files[{idx}], got {type(item).__name__}. "
						"Each entry must be a dict with keys: filename, content, (optional) directory, (optional) overwrite."
				)
		results: List[Dict[str, Any]] = []
		for item in files:
			results.append(self._write_single(item))
		return results

	def __call__(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		return self.run(files)

	def _run(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		return self.run(files)

class WebSearchTool(BaseTool):
    """A CrewAI-compatible tool that performs web searches using an underlying search API.

    This class subclasses `BaseTool` so it can be added to an Agent's
    `tools` list and validated by the crewai model.
    """

    name: str = "web-search-tool"
    description: str = "Perform web searches and return summarized results."

    _search_api: Any = None

    def __init__(self, search_api=None, **data):
        super().__init__(**data)
        self._search_api = search_api

    def run(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        if not self._search_api:
            return {"success": False, "error": "No search API configured."}

        try:
            results = self._search_api.search(query, num_results=num_results)
            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class Base64EncodeTool(BaseTool):
	"""Encode a string (or bytes) to base64.

	This tool is intended to be used by agents as a small helper step before
	calling the Batch File Writer Tool. Example flow:
	  1) Agent calls Base64EncodeTool with the file text -> returns content_b64
	  2) Agent includes returned content_b64 in the JSON array passed to
		 BatchFileWriterTool (key: content_b64)

	The tool returns a dict: {"success": True, "content_b64": "..."}
	or {"success": False, "error": "..."} on failure.
	"""

	name: str = "base64-encode"
	description: str = "Encode text or bytes to base64 (returns {'content_b64':...})."

	def run(self, text: Any) -> Dict[str, Any]:
		try:
			if isinstance(text, str):
				raw = text.encode("utf-8")
			elif isinstance(text, (bytes, bytearray)):
				raw = bytes(text)
			else:
				# Try to stringify non-string inputs
				raw = str(text).encode("utf-8")
			encoded = base64.b64encode(raw).decode("ascii")
			return {"success": True, "content_b64": encoded}
		except Exception as e:
			return {"success": False, "error": str(e)}
	def _run(self, text: Any) -> Dict[str, Any]:
		# BaseTool subclasses often require an _run implementation.
		# Delegate to run() for convenience so both sync and runtime
		# call paths work.
		return self.run(text)