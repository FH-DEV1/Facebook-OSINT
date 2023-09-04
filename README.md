# Facebook-OSINT

This repository was set to public because
⚠️This tool is depracated.⚠️

Simple yet powerful Facebook OSINT tool.

- [Disclaimer](#Disclaimer)
- [Installation](#Installation)
- [Usage](#Usage)
- [License](#License)

## Disclaimer <a name="Disclaimer"></a>

This tool is deprecated if you use -e arg or you abuse of the -i arg this tool will break because will get shadowbanned from the endpoint used to make this project work. However if you only use this tool responsibly with only -l and -i arg it should work correctly.

This project is under MIT License wich means the code is provided "as is" without any warranty. I'll add that this project is for educational purposes only and that I don't take any responsability for misusing. You may get banned for using this code.

## Installation <a name="Installation"></a>

First Clone the Repo with :

```
git clone https://github.com/FH-DEV1/Facebook-OSINT
```

Then Move into the Repo using :

```
cd Facebook-OSINT
```

Install dependencies using :

```
pip install -r requirements.txt
```

Create a JSON file to store the data :

```
echo [] > data.json
```

To finish installation you will need to get your headers/payload on line 53/54 of main.py.  
To do this go to https://www.facebook.com/login/identify/?ctx=recover&from_login_screen=0 open the Network console set preserve log to true and search a dummy input.  
You should see a request named "identify.php?ctx=recover".  
In this request first go to Headers and search for the requests headers X-Asbd-Id and X-Fb-Lsd replace the values of X-Asbd-Id and X-Fb-Lsd in line 53 with the correct values.  
Next go to Payload and copy the string that appears when you click view source on the Form Data paste it in line 54 and write {str(email)} to replace your dummy input.

## Usage <a name="Usage"></a>

To lookup if a phone number is associated with a facebook account in the facebook database you can run :

```
python main.py -i [PHONE]
```

To lookup if a username is associated with a phone number in the local database you can run :

```
python main.py -l "[USERNAME]"
```

-e arg will simply break the project.  
~~To extend the local database you can run :~~  
~~python main.py -e~~

## License <a name="License"></a>
MIT License

Copyright (c) 2023 FH.Dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
