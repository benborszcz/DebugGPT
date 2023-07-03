import config
import openai
import json
import backoff

# Set the API Params for OpenAI
openai.api_key = config.OPENAI_API_KEY

class Agent:
    def __init__(self, id, system: str = "You are a helpful assistant", additional_messages: list = None, functions: list = None):
        self.id = id
        self.system = system
        self.additional_messages = additional_messages
        self.functions = {}
        if functions != None:
            for function in functions:
                self.functions[function.name] = function
        else:
            self.functions = functions
    
    def generate(self, messages: list, temperature=0.1, presence_penalty=0.0, frequency_penalty=0.0, max_tokens=1000):      
        local_messages = []
        local_messages.extend(messages)
        local_messages.insert(0, {"role": "system", "content": self.system})
        if self.additional_messages != None: local_messages.insert(1, self.additional_messages)
        response = self.chat_completion(local_messages)
        return response
    
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def chat_completion(self, messages: list, temperature=0.4, presence_penalty=0.1, frequency_penalty=0.1, max_tokens=1000):
        # Generate a response using the OpenAI API
        if self.functions == None:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
            )
            return response
        else:
            passed_functions = []
            function_response = None
            for key, value in self.functions.items():
                passed_functions.append(value.to_dict())

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
                functions=passed_functions
            )
            response_message = response["choices"][0]["message"]
            if response_message.get("function_call"):
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                function_name = response_message["function_call"]["name"]
                fuction_to_call = self.functions[function_name]
                function_args = json.loads(response_message["function_call"]["arguments"])
                function_response = fuction_to_call.process_instruction(function_args)
                return {'choices': [{'message': {'content':function_response}}]}
            return response
    def chat_completion(self, messages: list, temperature=0.4, presence_penalty=0.1, frequency_penalty=0.1, max_tokens=1000):
        # Generate a response using the OpenAI API
        if self.functions == None:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
            )
            return response
        else:
            passed_functions = []
            function_response = None
            for key, value in self.functions.items():
                passed_functions.append(value.to_dict())

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
                functions=passed_functions
            )
            response_message = response["choices"][0]["message"]
            if response_message.get("function_call"):
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                function_name = response_message["function_call"]["name"]
                fuction_to_call = self.functions[function_name]
                function_args = json.loads(response_message["function_call"]["arguments"])
                function_response = fuction_to_call.process_instruction(function_args)
                return {'choices': [{'message': {'content':function_response}}]}
            return response
            