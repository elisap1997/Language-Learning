# ILR Language Proficiency Assessment Tool 🌐

A Python-based tool for self-assessing language proficiency according to the Interagency Language Roundtable (ILR) scale. This tool evaluates proficiency across four key language skills: Reading, Writing, Speaking, and Listening.

## Features 🚀

- Complete assessment across all four language skills
- Standard ILR-aligned scoring system (Levels 0 to 5)
- Progress tracking with JSON-based storage
- Multi-user support
- Historical results viewing
- User-specific result filtering

## Installation 📥

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ilr-assessment-tool.git
cd ilr-assessment-tool
```

2. Ensure you have Python 3.6+ installed
3. No additional dependencies required - the tool uses only Python standard library

## Usage 💡

Run the program using Python:
```bash
python ilr_quiz.py
```

### Menu Options:
1. Take Quiz - Start a new assessment
2. View All Results - Display all stored assessments
3. View Results by Username - Search for specific user's results
4. Exit - Close the program

### Rating Scale:
- 0 = Not at all
- 1 = Strongly Disagree
- 2 = Disagree
- 3 = Neutral
- 4 = Agree
- 5 = Strongly Agree

## ILR Proficiency Levels 📊

The tool evaluates proficiency according to these ILR levels:

| Level | Description |
|-------|-------------|
| 0 | No Proficiency |
| 0+ | Memorized Proficiency |
| 1 | Elementary Proficiency |
| 1+ | Elementary Proficiency, Plus |
| 2 | Limited Working Proficiency |
| 2+ | Limited Working Proficiency, Plus |
| 3 | Professional Working Proficiency |
| 3+ | Professional Working Proficiency, Plus |
| 4 | Full Professional Proficiency |
| 4+ | Full Professional Proficiency, Plus |
| 5 | Native or Bilingual Proficiency |

## Technical Details 🔧

### File Structure
- `ilr_quiz.py` - Main program file
- `ilr_quiz_results.json` - Results storage file (created automatically)

### Classes and Methods

#### ILRQuiz
Main class implementing the assessment functionality.

**Methods:**
- `run_quiz()`: Executes the assessment process
- `determine_level(score)`: Converts numerical scores to ILR levels
- `save_results(user_name, language, scores, levels)`: Stores assessment results
- `view_results(user_name=None)`: Displays stored results, optionally filtered by username

### Data Storage 💾

Results are stored in JSON format with the following structure:
```json
{
    "user_name": "string",
    "language": "string",
    "date": "YYYY-MM-DD HH:MM:SS",
    "scores": {
        "Reading": float,
        "Writing": float,
        "Speaking": float,
        "Listening": float
    },
    "levels": {
        "Reading": "string",
        "Writing": "string",
        "Speaking": "string",
        "Listening": "string",
        "Overall": "string"
    }
}
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Suggested areas for contribution:
- Additional language support
- GUI implementation
- Enhanced statistical analysis
- Result visualization
- Additional assessment criteria

## License 📄

[MIT](https://choosealicense.com/licenses/mit/)

## Author ✍️

[Your Name]

## Acknowledgments 🙏

- Based on the official ILR Skill Level Descriptions
- Inspired by language assessment needs in academic and professional contexts

---

## Changelog 📝

### Version 1.1.0
- Added 0 rating option for more accurate beginner assessment
- Implemented comprehensive result viewing functionality
- Added user-specific result filtering
- Enhanced score calculation accuracy

### Version 1.0.0
- Initial release
- Basic assessment functionality
- JSON-based result storage
- Multi-user support