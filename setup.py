from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='criticality',
   version='1.0',
   description='This package used to analyze neuron data for criticality.',
   license="",
   long_description=long_description,
   keywords='criticality, neuroscience, electrophysiology',
   package_dir={'criticality': 'criticality'},
   author='Keith Hengen, Sahara Ensley, Kiran Bhaskran-Nair,\
           Zhengyu Ma, Ralf Wessel\
           (Hengen Lab Washington University in St. Louis)',
   author_email='',
   maintainer='Kiran Bhaskaran-Nair, Sahara Ensley, Keith Hengen,\
           (Hengen Lab Washington University in St. Louis)',
   maintainer_email='',
   url="https://github.com/hengenlab/criticality_hlab",
   download_url="https://github.com/hengenlab/criticality_hlab",
   packages=['criticality'],
   install_requires=['ipython', 'numpy', 'matplotlib', 'seaborn', 'pandas',
                     'joblib', 'scipy', 'scikit-learn', 'glob2', 'powerlaw'],
   classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
   scripts=[
           ]
)
