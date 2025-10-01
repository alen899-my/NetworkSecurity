'''
this is a setup.py file for a Python package. It uses setuptools to define the package metadata and dependencies.define the package metadata and dependencies.

'''
from setuptools import find_packages,setup
from typing import List

def get_requirments()->List[str]:
    '''
    this function will return the list of requirments

    '''

    requirment_list:List[str]=[]
    try:
        with open("requirments.txt","r") as file:
            #read the file and return the list of requirments
            lines=file.readlines()
            #process each line
            for line in lines:
                requirment=line.strip()
                #ignore empty lines and -e ./
                if requirment and requirment!="-e .":
                    requirment_list.append(requirment)
    except FileNotFoundError:
        print(f"requirments.txt file not found!")
    return requirment_list
setup(
    name="networksecurity",
    version="0.0.1",
    author="Alen James",
    author_email="alenjames899@gmail.com",
    packages=find_packages(),
    install_requires=get_requirments(),
)