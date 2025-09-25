#!/Users/ashish/anaconda3/bin/python

import oci
import base64


#use your image & compartment id
compartmentId = "ocid1.compartment.oc1..aaaaaaaakbzxdecqyv3kawljq4rtcle6cdheaahqzjviysswyd4v43ocpzlq"
image_path = "my-image.jpeg"

llm_service_endpoint= "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
llm_client = None
llm_payload = None


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_message():
        content1 = oci.generative_ai_inference.models.TextContent()
        content1.text = "What is good and not good about the house in the picture"
        content2 = oci.generative_ai_inference.models.ImageContent()
        image_url = oci.generative_ai_inference.models.ImageUrl()
        image_url.url = f"data:image/jpeg;base64,{encode_image(image_path)}"
        content2.image_url = image_url
        message = oci.generative_ai_inference.models.UserMessage()
        message.content = [content1,content2]
        return message

def get_chat_request():
        chat_request = oci.generative_ai_inference.models.GenericChatRequest()
        #chat_request.preamble_override = "you always answer in a one stanza poem."
        #chat_request.message = get_message()
        chat_request.messages = [get_message()]
        chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
        chat_request.num_generations = 1
        chat_request.is_stream = False
        chat_request.max_tokens = 500
        chat_request.temperature = 0.75
        chat_request.top_p = 0.7
        chat_request.top_k = -1
        chat_request.frequency_penalty = 1.0
        return chat_request

def get_chat_detail (llm_request):
        chat_detail = oci.generative_ai_inference.models.ChatDetails()
        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="meta.llama-3.2-90b-vision-instruct")
        chat_detail.compartment_id = compartmentId
        chat_detail.chat_request = llm_request
        return chat_detail


CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('/home/hemant_gah/.oci/config', CONFIG_PROFILE)

llm_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
                config=config,
                service_endpoint=llm_service_endpoint,
                retry_strategy=oci.retry.NoneRetryStrategy(),
                timeout=(10,240))

chat_request = get_chat_request()
llm_payload =get_chat_detail(chat_request)
#llm_payload.chat_request.message = "why is the skyblue"

llm_response = llm_client.chat(llm_payload)
llm_text = llm_response.data.chat_response.choices[0].message.content[0].text
print("Question-> What is good and not good about the house in the picture")
print ("Response is->" + llm_text)