import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

prompt_beginning = "Given this transcription: "
prompt_end = """First, look over the transcription and create a refined transcription by reasonably matching to the keys of the mappings. It is okay if it does not match.
Then, convert the refined transcription to a list of ordered commands which are the values of the mappings. The transcribed commands should only exist within this mappping. If they are not, it is an invalid mapping.
The only exceptions are:
- when an integer is specified after the "for i in range" command. In this case, the command mapping should map
to "for i in range(specified_integer_value):" where specified_integer_value is the integer following the raw transcript that maps to the "for i in range" command. If the integer is 
in plain text, convert it to a number.
- when a condition is specified after "if" or "while". In this case, you should map to "if condition:" or "while condition:" where condition is the condition specified.

Return as a JSON for the keys 'isValid' if there is a valid mapping, 'commandList' for the list of commands, 'refinedTranscript' for the refined transcription,
and 'errorMessage' which is a string that describes why the mapping is invalid if it is invalid."""

# Examples to include: correct-simple, correct-hard, invalid-simple, invalid-edge
examples = [
    {
        "question": (prompt_beginning + "move turn left pick beeper put beeper move move" + prompt_end),
        "answer": "Json(isValid: True, commandList: ['move()', 'turn_left()', 'pick_beeper()', 'put_beeper()', 'move()', 'move()'], errorMessage: )"
    },
    {
        "question": (prompt_beginning + "move turn left for i in range ten" + prompt_end),
        "answer": "Json(isValid: True, commandList: ['move()', 'turn_left()', 'for i in range(10):'], errorMessage: )"
    },
    {
        "question": (prompt_beginning + "move right turn up turn left" + prompt_end),
        "answer": "Json(isValid: False, commandList: [], errorMessage: 'Invalid commands found in transcription: 'right', 'turn up'')"
    },
    {
        "question": (prompt_beginning + "I want to move up and turn right then turn left and then have a for loop that loops twelve times" + prompt_end),
        "answer": "Json(isValid: False, commandList: [], errorMessage: 'Invalid commands entered. Please respond according to the vocabulary and commands mappings')"
    },
]

example_prompt = PromptTemplate(
        input_variables=["question", "answer"], template="Question: {question}\n{answer}"
    )

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)

commands = {
    "move": "move()",
    "turn left": "turn_left()",
    "pick beeper": "pick_beeper()",
    "put beeper": "put_beeper()",
    # Added after testing
    "turn underscore left": "turn_left()",
    "pick underscore beeper": "pick_beeper()",
    "put underscore beeper": "put_beeper()",
    "for i in range": "for i in range",
    "for eye in range": "for i in range",
    "4i in range": "for i in range",
    # Expansion for conditions
    "front is clear": "front_is_clear()",
    "beepers present": "beepers_present()",
    "beepers in bag": "beepers_in_bag()",
    "left is clear": "left_is_clear()",
    "right is clear": "right_is_clear()",
    "front is blocked": "front_is_blocked()",
    "no beepers present": "no_beepers_present()",
    "no beepers in bag": "no_beepers_in_bag()",
    "left is blocked": "left_is_blocked()",
    "right is blocked": "right_is_blocked()",
    # Expansion for while, conditionals, function definition
    "if": "if",
    "else": "else:",
    "while": "while",
    # Expansion for commands
    "indent": "[indent]",
    "in dent": "[indent]",
    "dent": "[indent]",
    "tab": "[indent]",
    "unindent": "[unindent]",
    "backspace": "[backspace]",
    "run program": "[run]",
    "run": "[run]",
    "reset": "[reset]",
    "reset program": "[reset]",
    "enter": "[return]",
    "return": "[return]"
}

class Filter(BaseModel):
    isValid: bool = Field(description="Whether the transcription has valid command mapping")
    errorMessage: str = Field(description="Error message describing what is wrong with mapping")
    commandList: list[str] = Field(description="List of commands from the transcription")
    refinedTranscript: str = Field(description="Transcription after being refined to match with keys of mappings")

class LLMChain():
    def __init__(self, model_name = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0, api_key=os.environ['OPENAI_API_KEY'])
        self.structured_llm = self.llm.with_structured_output(Filter, method="json_mode")
    
    def llm_call(self, query: str):
        """
        Standard llm call returning completion
        """
        
        return self.llm.invoke(query)
    
    def structured_llm_call(self, query, type = "mapping"):
        """
        Structured LLM Call given a query and mapping
        """
        input = prompt_beginning + query + prompt_end + "This is the mappping: " + str(commands)
        
        return self.structured_llm.invoke(prompt.format(input=input))


    


    
