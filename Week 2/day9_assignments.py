import anthropic
client=anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")

product="Bangladesh Map Puzzle"

#example of zero shot
zero_shot=client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=200,
    messages=[
        {"role":"user","content":f"একটা ভালো product description লিখো {product} এর জন্য"}
    ]
)

#example of few-shot
product_info=f"""
    এই স্টাইলে product description লিখো:

            Example:
            Product: Alphabet Blocks
            Description: শিশুদের জন্য মজার শেখার খেলনা! রঙিন ব্লক দিয়ে A-Z শিখুন সহজে।

            এখন লিখো:
            Product: {product}
            Description:
"""
instruction = "উপরের তথ্য দিয়ে একটা আকর্ষণীয় Facebook ad caption লিখো।"
few_shot=client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    messages=[
        {
        "role":"user",
         "content": product_info + "\n" + instruction
         
         }
    ]
)

#example of chain of thaught
chain_of_thought=client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    messages=[
        {
            "role":"user",
            "content":"আমার পণ্যের দাম ৩০০ টাকা, কিন্তু প্রতিযোগী বিক্রি করছে ২৫০ টাকায়। step by step ভেবে বলো আমি কী করব।"
        }
    ]

)

#example of role play

role_play=client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    system="তুমি একজন বিখ্যাত copywriter, তোমার caption সবসময় viral হয়",
    messages=[
        {
        "role":"user",
         "content":f"আমার {product} এর জন্য একটা Facebook ad caption লিখে দাও"
         }
    ]
)



print("zero shot:\n",zero_shot.content[0].text)
print("few shot:\n",few_shot.content[0].text)
print("chain of thought\n",chain_of_thought.content[0].text)
print("role play\n",role_play.content[0].text)