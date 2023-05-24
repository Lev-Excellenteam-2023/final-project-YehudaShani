# secret key is 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

import openai
import asyncio
import file_writer

from parser import Parser, get_text_from_slide

openai.api_key = "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"


def generate_summary(parser: Parser):
    messages_to_send = []
    messages_to_send.append({"role": "assistant", "content": "you are a chatbot that explains bullet points in a "
                                                             "powerpoint presentation to a student, only be informative, not friendly"})
    for number, slide in enumerate(parser):
        text = get_text_from_slide(slide)
        if len(text) == 0:
            continue
        content = " ".join(get_text_from_slide(slide))
        messages_to_send.append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send
        )

        chat_response = completion.choices[0].message.content
        messages_to_send.append({"role": "assistant", "content": chat_response})

        yield (number, chat_response)


async def get_gpt_answer(parser, file_name):
    generator = generate_summary(parser)
    writer = file_writer.FileWriter(file_name)
    while True:
        try:
            slide_number, text = next(generator)
            print("Writing slide number", slide_number)
            writer.write_to_file(slide_number, text)
            await asyncio.sleep(20)
        except StopIteration:
            writer.close_file()
            break
        except Exception as e:
            print(e)
            continue
