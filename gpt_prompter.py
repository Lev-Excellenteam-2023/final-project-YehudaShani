# secret key is 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

import openai
import asyncio
import file_writer

from parser import Parser, get_text_from_slide

openai.api_key = "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"


def generate_summary(parser: Parser):
    """
    Generate a summary of the presentation.
    :param parser: The parser object that holds the slides.
    :return: a generator that yields the slide number and the summary of the slide.
    """

    messages_to_send = [{"role": "assistant", "content": "Hello, I am your assistant, i will explain these topics."}]
    for number, slide in enumerate(parser):
        text = get_text_from_slide(slide)
        if len(text) == 0:
            continue
        content = " ".join(get_text_from_slide(slide))
        messages_to_send.append({"role": "user", "content": "Summarize and explain these topics: " + content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send
        )

        chat_response = completion.choices[0].message.content
        messages_to_send.append({"role": "assistant", "content": chat_response})

        yield number, chat_response


async def get_gpt_answer(parser, file_name):
    """
    Get the GPT answer and write it to a file.
    :param parser: The parser object.
    :param file_name: The name of the file to write to.
    :return: None
    """
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
            break
