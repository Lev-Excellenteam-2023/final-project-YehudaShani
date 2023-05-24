# secret key is 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

import openai
import asyncio

from parser import Parser, get_text_from_slide

openai.api_key = "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"


def generate_summary(parser: Parser):
    messages_to_send = []
    messages_to_send.append({"role": "assistant", "content": "you are a chatbot that explains bullet points in a "
                                                             "powerpoint presentation to a student"})
    for slide in parser:
        get_text_from_slide = get_text_from_slide(slide)
        if len(get_text_from_slide) == 0:
            continue
        content = " ".join(get_text_from_slide(slide))
        messages_to_send.append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send
        )

        chat_response = completion.choices[0].message.content
        messages_to_send.append({"role": "assistant", "content": chat_response})

        yield chat_response


async def get_gpt_answer(parser):
    generator = generate_summary(parser)
    while True:
        try:
            yield next(generator)
            await asyncio.sleep(20)
        except StopIteration:
            break
