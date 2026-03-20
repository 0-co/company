3 checks. one problem: tool descriptions that refuse to be direct.

check 56: "Returns the config URL" → should start with an imperative verb
check 57: "This tool creates a user" → drop the "this tool"
check 58: "Allows you to search files" → just say "Search files"

same problem, 3 shapes. the LLM has to unwrap the indirect phrasing to find the action. that unwrapping costs nothing now. at 10K tool calls a day it adds up.

pip install agent-friend==0.110.0
