# ASDF: A Differential Testing Framework for ASR Systems

Automatic testing tools for Automatic Speech Recognition (ASR) systems are used to uncover failed test cases using  ASDF is a differential testing framework for ASR systems. ASDF leverages upon [CrossASR++](https://github.com/soarsmu/CrossASRplus), an existing ASR testing tool that automates the audio test case generation process, and further improves it by incorporating differential testing methods. CrossASR++ selects texts from an input text corpus, converts them into audio using a Text-to-Speech (TTS) service, and uses the audio to test the ASR systems. However, the quality of these tests greatly depend on the quality of the text corpus provided, and may not uncover underlying weaknesses of the ASRs due to the text's limited variation and vocabulary. 

Here, ASDF builds upon CrossASR++ by incoprporating differential testing for ASR systems by applying text transformation methods to the original text inputs that failed in the CrossASR++ ASR testing process, effectively creating new high-quality test cases for ASR systems. The text transformation methods used are homophone transformation, augmentation, plurality transformation, tense transformation and adjacent deletion. We also improved analysis by providing high-level summaries of failed test cases and a graph of phonemes in the text input against their frequency of failure. Finally, we improved the tool's usability by including a CLI for easier use. 

Please check out our Tool Demonstration video and PDF preprint.

## Transformation Methods
1. **Homophone Transformation**: Identifies the error-inducing term of the failed test case. Following that, a homophone of the error-inducing term is found, and an example sentence that contains that homophone is obtained through the usage of an online dictionary API. The example sentence will then be used as the new test case. Only transforms texts with an error-inducing term that has a homophone. Each homophone will produce a new test case.

2. **Augmentation**: Randomly inserts words into the failed test case through contextual word embedding. After insertion, the sentence is used as the new test case. Does not use the error-inducing term in its text transformation process.

3. **Adjacent Deletion**: Identifies the error-inducing term of the failed test case. Subsequently, the words adjacent to the error-inducing term in the sentence are deleted. The sentence after the deletion is then used as the new test case. Produces the same number of test cases as the number of error-inducing terms with each test case deleting adjacent words from a single error-inducing term. 

4. **Plurality Transformation**: Identifies the error-inducing term of the failed test case. It then converts the error-inducing terms in the failed test case from singular nouns to plural nouns. Only transforms texts with an error-inducing term that is a noun. Produces a single test case output with all error-inducing nouns transformed.

5. **Tense Transformation**: Identifies the verbs that express the grammatical tense and changes them to the past tense. Does not use the error-inducing term in its text transformation process. Produces a single test case with all error-inducing verbs transformed.

### Example Transformations

| Original Text | Error Terms |
|---|---|
| this has been done in no less than fifteen member states and through the medium of twelve community languages | in, fifteen, member |


| Text Transformation Method | Affected Terms | Transformed Text | 
|---|---|---|
| **Homophone Transformation** | First error term homophone transformation: *in* | the *inns* of court the *inns* of chancery serjeants *inns* |
| **Augmentation** | - | this *service* has been *being* done in no less than *his* fifteen member states and *varies* through the medium of *nearly* twelve community *spoken* languages |
| **Adjacent Deletion** | First error term adjacent deletion: *done, no* | this has been in less than fifteen member states and through the medium of twelve community languages |
| **Plurality Transformation** | All error-inducing nouns: *in, fifteen, member* | this has been done *ins* no less than *fifteens* *members* states and through the medium of twelve community languages |
| **Tense Transformation** | All verbs: *has, been, done* | this *had* *was* *did* in no less than fifteen member states and through the medium of twelve community languages |

*Note: For Homophone Transformation and Adjacent Deletion, other test cases can be created based on the other error-inducing terms. However, there are no homophones for **fifteen** or **member** and only produces a single test case for **in**. For Adjacent Deletion, the other two test cases are not shown.*

## Initial Setup

### WSL
1. Set up WSL to use Linux in Windows. [Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
2. To access Window files in WSL: WSL mounts your machine's fixed drives under the /mnt/<drive> folder in your Linux distros. For example, your C: drive is mounted under /mnt/c/
3. It is recommended to store your local repo under your Linux distro home directory instead of /mnt/<drive>/... because differing file naming systems will cause issues (eg. filename is not case sensitive in Windows file system)
4. To connect to the Internet, change the `nameserver` in `etc/resolv.conf` to 8.8.8.8. [Stackoverflow](https://stackoverflow.com/questions/62314789/no-internet-connection-on-wsl-ubuntu-windows-subsystem-for-linux)
5. `etc/resolv.conf` will reset everytime you restart WSL. To solve this issue, look at this [post](https://askubuntu.com/questions/1347712/make-etc-resolv-conf-changes-permanent-in-wsl-2)

### Docker Desktop
1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. If you are using WSL, set up Docker Desktop for Windows with WSL 2. [Guide](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers)

## Usage
1. Go to the `example` directory using: `cd asdf-differential-testing/CrossASRplus/examples`
2. Execute the `start.bat` batch file
3. Follow the prompts to customise execution

For certain selections, the default settings are used if not specified by the user:
- Input corpus file path: `CrossASRplus/examples/corpus/50-europarl-20000.txt`
- Output file path: `CrossASRplus/examples/output/default`
- ASRs: `deepspeech`, `wav2letter`, `wav2vec`
- Number of texts to be processed: 100

## Results
Once testing is compeleted, a folder containing the results can be found within the `output` directory named as specified by user input. If none is specified, it is defaulted to `CrossASRplus/examples/output/default`.

Four folders are created within this directory:
1. `case`: Contains nested folders of the format `<tts_name>/<asr_name>/<test_case_no>.txt` containing text files indicating the result of each test case for each individual ASR. `0` indicates an indeterminable test case, `1` indicates a failed test case and `2` indicates a successful test case.
2. `data`: Contains two nested folders of the format `audio/<tts_name>` and `transcription/<tts_name>/<asr_name>` which holds the audio files produced from the TTS and transcriptions of the audio by each individual ASR respectively.
3. `execution_time`: Contains two nested folders of the format `audio/<tts_name>` and `transcription/<tts_name>/<asr_name>/<test_case_no>` which contains text files indicating the time taken to produce each test case's audio and transcription by each ASR respectively.
4. `result`: Contains a nested folder of the format `<tts_name>/<asr_name_1_asr_name_2_...asr_name_n>/num_iteration_2/text_batch_size_global` which contains six files:
    1. `all_test_cases.json`: JSON file which has a key for each iteration containing an array value detailing the outcome of each text input.
    2. `indeterminable.json`: JSON file detailing the statistics of indeterminable test cases.
    3. `without_estimator.json`: JSON file detailing the statistics of failed test cases.
    4. `failed_test_cases_analysis.txt`: Text file detailing the performance the ASRs using 10 different metrics.
    5. `phoneme_graph.pdf`: PDF file graphing each phoneme within the processed text corpus and its respective frequency of failure.
    6. `asr_comparison.csv`: CSV file containing two different tables for self-analysis, failed cases per ASR and failed cases per text input.
    
### Metrics
10 metrics can be found within `failed_test_cases_analysis.txt`. A failed text is defined as an input text that was incorrectly transcribed by at least one ASR service. A text input must be transcribed correctly by at least one ASR service to be deemed valid (or determinable); otherwise, it is deemed as indeterminable and is discarded. A failed case, on the other hand, is defined as a specific text output from an individual ASR service that does not match its corresponding input text.  
    
1. `corpus_failed_cases_percentage`: Percentage of failed cases from the input corpus only.
2. `corpus_failed_text_percentage`: Percentage of failed texts from the input corpus only.
3. `total_corpus_failed_cases`: Total number of failed cases from the input corpus.
4. `total_corpus_failed_text`: Total number of failed texts from the input corpus.
5. `total_corpus_text`: Total number of texts from the input corpus.
6. `total_transformed_failed_cases`: Total number of failed cases from transformed texts.
7. `total_transformed_failed_text`: Total number of failed texts from transformed texts.
8. `total_transformed_text`: Total number of transformed texts.
9. `transformed_failed_cases_percentage`: Percentage of failed cases from transformed texts only.
10. `transformed_failed_text_percentage`: Percentage of failed texts from transformed texts only.

## Example Analysis
Some of the analysis that can be done by graphing the data in the CSV file are as follows:

<img src="images/per_asr.png" width="630" height="400"></img> \
*Example 1: Failed test cases per ASR, where ASRs which are more failure-prone can be identified*


<img src="images/per_text_input.png" width="700" height="400"></img> \
*Example 2: Failed test cases per text input, where areas in the input corpus which cause the most failures can be analysed*
