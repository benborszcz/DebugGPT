# DebugGPT

DebugGPT is a Python-based debugging tool that leverages OpenAI's GPT-3.5 model to help debug Python scripts. It analyzes error codes, identifies the files involved, and explains the error in natural language. It also provides a step-by-step plan to solve the problem, generates the necessary code to fix the error, and applies the changes to the script. After applying the changes, DebugGPT will re-run the script to check if the changes have improved the script or solved the errors.

## Future Developments

We aim to extend DebugGPT's capabilities to handle multiple programming languages including JavaScript, Java, and others. We also plan to incorporate human input for complex problem-solving, enable system-level interactions like installing necessary packages, and add the ability to search the web for solutions and necessary downloads. Speed optimization is also a key focus area in our roadmap.

## Installation

DebugGPT requires Python 3.6 or later. You start by cloning the repository:

```bash
git clone https://github.com/benborszcz/DebugGPT.git
cd DebugGPT
```

Before you start using DebugGPT, you need to set up your OpenAI API key. Create a `.env` file in the root directory of the project and add your OpenAI API key like this:

```bash
OPENAI_API_KEY=your-api-key-here
```

Now run pip install:
```bash
pip install .
```
## Usage

To use DebugGPT, simply run the `dgpt` command followed by the path to the Python script you want to debug:

```bash
dgpt script.py -s
```
Use -v for verbose and -s for slim. We recommend -s for normal use and -v for more complicated errors or learning how the tool works.

DebugGPT will run the script, analyze any errors that occur, and provide a step-by-step plan to fix them. It will then generate the necessary code to fix the errors and apply the changes to the script. After applying the changes, DebugGPT will re-run the script to check if the changes have improved the script or solved the errors.

If the script still contains errors after the changes have been applied, DebugGPT will analyze the new errors and repeat the process. It will continue to do this until all errors have been fixed or the user decides to stop the debugging process.

## License

DebugGPT is released under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions to DebugGPT are welcome! Please see the ROADMAP.md file for more details.

## Contact

If you have any questions or feedback, please feel free to contact us.

## Acknowledgements

DebugGPT is not possible without the amazing work of the OpenAI team on the GPT-3.5 model. We would like to express our gratitude to them for making such a powerful tool available to the public.

## Example
https://user-images.githubusercontent.com/88807186/250950217-66b1b5f1-11b0-4bbc-8242-84e5c7a83eb0.mov
