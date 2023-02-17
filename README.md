Image-Scanner 👁‍🗨
===
Open-source project that use Drype to create a Vulnerability scan report for a choosen image.
## Informations  ☕️
- Title:  `image-scanner`
- Author:  `hz59`
- email: [coming soon]()

## Install & Dependence  🚀
- python3
- grype: https://github.com/anchore/grype.git 

## Getting started ▶️
- Scan a choosen image using drype and save the output in a txt file:
  ```
  grype choosen/image:tag > scan-result.txt
  ```
- Run the python script to render the result in a html file stylized:
  ```
  python3 txt2html.py
  ```
- Open this file in a browser:
  ```
  output.html
  ```
## Directory Hierarchy
```
|—— output.html
|—— scan-result.txt
|—— txt2html.py
```
## Code supported ☀️
### Tested with
  ```
  - Python: 3.9.5
  - Grype: 0.57.1
    - Syft Version: 0.72.0
  ```
## Next versions ⚗️
| Features | When |
| ---     | ---   |
| Improve the html results | Next soon |
| Improve python script with prompt | Next soon |
| Docker-compose to launch the project | Next |

## References 🖇
- [https://github.com/anchore/grype.git ]() 🐙
- [https://www.python.org/downloads/]() 🐍

## For contributions 🌟
Create a push request of updates related to WIP features with a review request.
  
## License
Open-source project all developed by hz59 - 2023.


