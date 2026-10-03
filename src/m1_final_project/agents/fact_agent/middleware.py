from langchain.agents.middleware import ModelRequest, dynamic_prompt

from m1_final_project.quiz.prompts import JUDGE_SYSTEM


@dynamic_prompt
def set_fact_agent_system_prompt(req: ModelRequest) -> str:
    voice = req.runtime.context.voice

    system_prompt = JUDGE_SYSTEM.format(voice=voice)

    return system_prompt
