import json
import os

TXT_PATH = 'questions/Kompyuter tarmoqlari Hemisga Test (250 ta).txt'
JSON_PATH = 'input/quiz_questions.json'

def parse_txt_to_json(txt_path, json_path):
	with open(txt_path, 'r', encoding='utf-8') as f:
		content = f.read()

	# Split questions by '++++' delimiter
	raw_questions = [q.strip() for q in content.split('++++') if q.strip()]
	questions = []
	for raw in raw_questions:
		# Find all answer options
		parts = [p.strip() for p in raw.split('====') if p.strip()]
		if not parts or len(parts) < 2:
			continue
		question_text = parts[0]
		options = []
		correct_option_id = None
		for idx, opt in enumerate(parts[1:]):
			if opt.startswith('#'):
				options.append(opt[1:].strip())
				correct_option_id = idx
			else:
				options.append(opt.strip())
		if correct_option_id is None:
			continue  # skip if no correct answer
		questions.append({
			'question': question_text,
			'options': options,
			'correct_option_id': correct_option_id
		})

	# Ensure output directory exists
	os.makedirs(os.path.dirname(json_path), exist_ok=True)
	with open(json_path, 'w', encoding='utf-8') as f:
		json.dump(questions, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
	parse_txt_to_json(TXT_PATH, JSON_PATH)
