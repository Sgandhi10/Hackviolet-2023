prompt2 = "Given these political committees: " + subcommittees + "Rank the committees based on how relevant they are to the following text in a python-styled list like so x,y,z:" + paragraph
response2 = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt2,
  temperature=0
)