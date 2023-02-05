import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.Model.list()
title = "Chinese government shooting baloon"
paragraph = "chinese army will attack america in less than twenty days"
prompt = "Given these political committees: Transportation and Infrastructure, Judiciary, Science, Space, and Technology, Commerce, Science and Transportation, Indian Affairs , Strategic Competition between the United States and the Chinese Communist Party , Ways and Means, Veterans Affairs, Ethics, Financial Services, Budget, Natural Resources, Banking, Housing and Urban Affairs, Rules and Administration, House Administration, Education and the Workforce, Aging , Energy and Commerce, Small Business and Entrepreneurship, Finance, Homeland Security, Small Business, Oversight and Accountability, Ethics , Homeland Security and Governmental Affairs, Foreign Affairs, Tom Lantos Human Rights Commission, International Narcotics Control , Foreign Relations, Energy and Natural Resources, Agriculture, Rules, Health, Education, Labor and Pensions, Environment and Public Works, Intelligence , Agriculture, Nutrition and Forestry, Appropriations, Armed Services. Tell me which 3 committees are most relevant to the following text separated by commas (i.e. x,y,z): \n" + title + "\n" + paragraph
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0
)
print(response['choices'][0]['text'])