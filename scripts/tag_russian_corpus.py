"""
This script allows to tag a Russian corpus with information about
1st person gender, 2nd person gender, and the politeness level.
"""

import re
import sys

import spacy

nlp = spacy.load("ru_core_news_sm")

first_person_gender = [
    # past-tense verbs
    (r'\bя \w+[^ую]_(AUX|VERB)_F\b', '<1f>'),
    (r'\bя \w+[^ую]_(AUX|VERB)_M\b', '<1m>'),
    (r'\bя [^,\.:\t\n]*?[^ую]_(AUX|VERB)_F\b', '<1f>'),
    (r'\bя [^,\.:\t\n]*?[^ую]_(AUX|VERB)_M\b', '<1m>'),
    (r'_(AUX|VERB)_F я\b', '<1f>'),
    (r'_(AUX|VERB)_M я\b', '<1m>'),
    # adjectives, nouns, and complements
    (r'\bя [^и][^,\.:\t\ncG]*?_(ADJ|DET)_F\b', '<1f>'),
    (r'\bя [^и][^,\.:\t\ncG]*?_(ADJ|DET)_M\b', '<1m>'),
    (r'\bя (\w+ )?(бы|ста|выгля|иду|пойд|оста|чувству)\w* \w+_(ADJ|NOUN|DET)_F_Ins', '<1f>'),
    (r'\bя (\w+ )?(бы|ста|выгля|иду|пойд|оста|чувству)\w* \w+_(ADJ|NOUN|DET)_M_Ins', '<1m>'),
    (r'\bя (- )?([^и]\w+ )?\w+_(ADJ|DET|NOUN)_F_Nom', '<1f>'),
    (r'\bя (- )?([^и]\w+ )?\w+_(ADJ|DET|NOUN)_M_Nom', '<1m>'),
    # past-tense verbs (without morphology tags)
    (r'\bя (\w+ )*?\w+ла(сь)?(\b|_)', '<1f>'),
    (r'\bя (\w+ )*?\w+[аяиыуеё]л(ся)?(\b|_)', '<1m>'),
    # verbs and adjectives without explicit subject
    (r'\bя \w+_VERB\w* , что \w+_(AUX|VERB)_F', '<1f>'),
    (r'\bя \w+_VERB\w* , что \w+_(AUX|VERB)_M', '<1m>'),
    (r'\w+[ую](сь)?_VERB\w* , (потому )?что \w+_(AUX|VERB)_F', '<1f>'),
    (r'\w+[ую](сь)?_VERB\w* , (потому )?что \w+_(AUX|VERB)_M', '<1m>'),
    (r'^рада\b', '<1f>'),
    (r'^рад\b', '<1m>'),
    (r'^никогда не \w+ла(сь)?_VERB_F', '<1f>'),
    (r'^никогда не \w+л(ся)?_VERB_M', '<1m>'),
    (r'\bя (\w+ )?(принёс|провёл|шёл|пришёл|пошёл)(\b|_)', '<1m>'),
    (r'^(-_\w+ |не |наверное , )?\w+[аяиыуеё]ла(сь)?.*\.$', '<1f>'),
    (r'^(-_\w+ |не |наверное , )?\w+[аяиыуеё]л(ся)?.*\.$', '<1m>'),
    (r'^(- )?уверена_\w+ .*\.', '<1f>'),
    (r'^(- )?уверен_\w+ .*\.', '<1m>'),
    # complement of transitive verbs
    (r'(дела|счита|вид|виж|назнач|зна|бы|встрет)\w* меня \w+[ое]й_(ADJ|DET|NOUN)_F_Ins', '<1f>'),
    (r'(дела|счита|вид|виж|назнач|зна|бы|встрет)\w* меня \w+[ыи]м_(ADJ|DET|NOUN)_M_Ins', '<1m>')
]


second_person_gender = [
    # past-tense verbs
    (r'\bты \w+_(AUX|VERB)_F\b', '<2f>'),
    (r'\bты \w+_(AUX|VERB)_M\b', '<2m>'),
    (r'\bты [^,\.:\t\n]*?_(AUX|VERB)_F\b', '<2f>'),
    (r'\bты [^,\.:\t\n]*?_(AUX|VERB)_M\b', '<2m>'),
    (r'_(AUX|VERB)_F ты\b', '<2f>'),
    (r'_(AUX|VERB)_M ты\b', '<2m>'),
    # adjectives, nouns, and complements (singular)
    (r'\bты [^и][^,\.:\t\ncG]*?_(ADJ|DET)_F\b', '<2f>'),
    (r'\bты [^и][^,\.:\t\ncG]*?_(ADJ|DET)_M\b', '<2m>'),
    (r'\bты (\w+ )?(бы|ста|выгляд|пойд|оста|чувству|возвраща)\w* \w+_(ADJ|NOUN|DET)_F_Ins', '<2f>'),
    (r'\bты (\w+ )?(бы|ста|выгляд|пойд|оста|чувству|возвраща)\w* \w+_(ADJ|NOUN|DET)_M_Ins', '<2m>'),
    (r'\bты (- )?([^и]\w+ )?\w+_(ADJ|DET|NOUN)_F_Nom', '<2f>'),
    (r'\bты (- )?([^и]\w+ )?\w+_(ADJ|DET|NOUN)_M_Nom', '<2m>'),
    # past-tense verbs (without morphology tags, 1st part)
    (r'\bты (\w+ )*?\w+ла(сь)?(\b|_)', '<2f>'),
    (r'\bты (\w+ )*?\w+[аяиыуеё]л(ся)?(\b|_)', '<2m>'),
    # verbs and adjectives without explicit subject (1st part)
    (r'\b(ты \w+_VERB\w*|спасибо\w*)( ,)? что \w+_(AUX|VERB|ADJ)_F', '<2f>'),
    (r'\b(ты \w+_VERB\w*|спасибо\w*)( ,)? что \w+_(AUX|VERB|ADJ)_M', '<2m>'),
    (r'\w+шь(ся)?_VERB\w* , (потому )?что \w+_(AUX|VERB)_F', '<2f>'),
    (r'\w+шь(ся)?_VERB\w* , (потому )?что \w+_(AUX|VERB)_M', '<2m>'),
    # adjectives, nouns, and complements (plural)
    (r'\bвы (\w+ )?(бы|ста|выгляд|пойд|оста|чувству|возвраща)\w* \w+_(ADJ|NOUN|DET)_F_Ins', '<2f>'),
    (r'\bвы (\w+ )?(бы|ста|выгляд|пойд|оста|чувству|возвраща)\w* \w+_(ADJ|NOUN|DET)_M_Ins', '<2m>'),
    (r'\bвы (- )?(\w+ )?\w+_(ADJ|DET|NOUN)_F_Nom', '<2f>'),
    (r'\bвы (- )?(\w+ )?\w+_(ADJ|DET|NOUN)_M_Nom', '<2m>'),
    (r'\bвы [^,\.:\t\ncG]*?_(ADJ|DET)_F\b', '<2f>'),
    (r'\bвы [^,\.:\t\ncG]*?_(ADJ|DET)_M\b', '<2m>'),
    # adjectives, nouns, and complements with the imperative
    (r'\b(будь)(те)?\w* (ты )?\w+_(ADJ|NOUN|DET)_F(_Ins|\b)', '<2f>'),
    (r'\b(будь)(те)?\w* (ты )?\w+_(ADJ|NOUN|DET)_M(_Ins|\b)', '<2m>'),
    # verbs and adjectives without explicit subject (2nd part)
    (r'поняла_\w+ (меня )?\?', '<2f>'),
    (r'понял_\w+ (меня )?\?', '<2m>'),
    # past-tense verbs (without morphology tags, 2nd part)
    (r'\bты (\w+ )?(принёс|провёл|шёл|пришёл|пошёл)(\b|_)', '<2m>'),
    # words of address
    (r'(?<=[,\.?!] )(дорогая|дорогуша|любимая|милая|миленькая|маленькая|подруга|сладкая)_\w+ '\
        r'([,\.?!]|моя)', '<2f>'),
    (r'(?<=[,\.?!] )(дорогой|любимый|милый|маленький|дружище|сладкий)_\w+ ([,\.?!]|мой)', '<2m>'),
    (r'\bмоя_\w+ (дорогая|дорогуша|любимая|милая|миленькая|маленькая|подруга|сладкая) [,\.?!]',
        '<2f>'),
    (r'\bмой_\w+ (дорогой|любимый|милый|маленький|друг|дружище|сладкий) [,\.?!]', '<2m>'),
    # verbs and adjectives without explicit subject (3rd part)
    (r'^(-_\w+ |не |наверное , )?\w+[аеия]ла(сь)?.*\?$', '<2f>'),
    (r'^(-_\w+ |не |наверное , )?\w+[аеия]л(ся)?.*\?$', '<2m>'),
    (r'^(- )?уверена_\w+ .*\?', '<2f>'),
    (r'^(- )?уверен_\w+ .*\?', '<2m>'),
    # complement of transitive verbs
    (r'(дела|счита|вид|виж|назнач|зна|бы|встрет)\w* тебя \w+[ое]й_(ADJ|DET|NOUN)_F_Ins', '<2f>'),
    (r'(дела|счита|вид|виж|назнач|зна|бы|встрет)\w* тебя \w+[ыи]м_(ADJ|DET|NOUN)_M_Ins', '<2m>')
]


politeness_level = [
    # singular pronouns
    (r'\b(ты|тебя|тебе|тобой|тобою|тво\w{,3})(\b|_)', '<T>'),
    # imperative singular
    (r'(VERB|AUX)_Imp_Sing', '<T>'),
    (r'([^и]йся|[^лп]ись)(_|\b)', '<T>'),
    # explicit list of singular imperatives
    (r'\b(от|за|по|на|из|у|о|про|пере|при|с|до|вы)?'\
        r'(молчи|моги|груби|вини|звони|повесь|годи|пей|крой|пробуй|пусти|прощай|подмети|держи|'\
        r'возьми|лезай|стой|веди|лей|бери|крывай|ставай|мешай|саживай|лги|спроси|прекрати|угадай|'\
        r'трогай|здравствуй|беги|стой|слыши|смотри|отойди|читай|лезай|станови|слушай|жалуй|спи|'\
        r'взгляни|йди|иди|глупи|раскажи|скажи|прости|целуй|пой|зволяй|убей|дай|будь|ставь|'
        r'ешь)(\b|_)',
        '<T>'),
    # plural pronouns
    (r'\b(вы|вас|вам|вами|ваш\w{,3})(\b|_)', '<V>'),
    # imperative plural
    (r'(VERB|AUX)_Imp_Plur', '<V>'),
    (r'(?<!ивр)[ияй]те(сь)?(\b|_)', '<V>'),
    # 2nd person plural verb forms
    (r'(знаете|можете)', '<V>')
]

def guess_tag(string, rules):
    """
    Guess the suiting tag for a string given a hierarchical set of rules.

    Args:
        string: the string to analyze.
        rules: a list of tuples, each containing a regular expression and a tag.

    Returns:
        str: the tag for the first match in the rule set.
    """

    for regex, tag in rules:
        if re.search(regex, string, re.IGNORECASE):
            return tag
    return ''


def annotate_morphology(string):
    """
    Annotate relevant morphological tags to each token in a string.

    Args:
        string: the string to annotate.

    Retuns:
        str: the morphology-annotated string.
    """

    doc = nlp(string)
    tokens = []
    for token in doc:
        gender = token.morph.get('Gender')
        animacy = token.morph.get('Animacy')
        case = token.morph.get('Case')
        case = '_' + case[0] if case != [] else ''
        mood = token.morph.get('Mood')
        number = token.morph.get('Number')
        if mood != []:
            mood = '_' + mood[0] + '_' + number[0] if mood[0] == 'Imp' else ''
        else:
            mood == ''
        if gender == []:
            if mood == []:
                tokens.append(f'{token.text}')
            else:
                tokens.append(f'{token.text}_{token.tag_}{mood}')
        elif animacy == []:
            tokens.append(f'{token.text}_{token.tag_}_{gender[0][0]}{case}')
        else:
            anim = '_' + animacy[0] if animacy[0] == 'Anim' else ''
            tokens.append(f'{token.text}_{token.tag_}_{gender[0][0]}{case}{anim}')
    return ' '.join(tokens)


def main():
    """
    Open the input file and tag each line with the 1st person gender, 2nd person gender
    and politeness level.
    """

    counter = 0
    with open(sys.argv[1]) as corpus, open(sys.argv[2], 'w') as outfile:
        for line in corpus:
            counter += 1
            line_annotated = annotate_morphology(line)
            first_person = guess_tag(line_annotated, first_person_gender)
            second_person = guess_tag(line_annotated, second_person_gender)
            politeness = guess_tag(line_annotated, politeness_level)
            outfile.write(f'{first_person}\t{second_person}\t{politeness}\t{line}')
    print(f'Done. Processed {counter} lines.')

if __name__ == '__main__':
    main()
