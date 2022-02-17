"""
This script allows to tag a French corpus with information about
1st person gender, 2nd person gender, and the politeness level.
"""

import re
import sys

import spacy

nlp = spacy.load("fr_core_news_sm")

_ = r'(_\w+)?'
articles = rf'(une?|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?){_}'
negation = r"(pas|plus|jamais|guère|que|qu '|ni)"
adverbs = rf"(plus|moins|assez|très|beaucoup|trop|un peu|tant|encore|si|déjà|aussi|toujours|"\
    rf"juste|peut-être|plutôt|en quelque sorte|d ' abord|presque|bien|même|tout à fait|"\
    rf"à peine|donc|encore|quand même|quasi|tout autant|à nouveau|\w+ment(_\w+)?){_}"
suffix_fem = r"(ère|[auè]le|eu[rs]e|ai[ns]e|ète|lle|tte|sse|nne|ive|[ûu]re|gue|trice|gne|ouse)"
suffix_masc = r"([ea]l|\won|[^b]ien|if|\wé|[^s]ou|[^v]\wc|eau|[bdgptcslmnrv]é|[bdgptcslmnrv]i|"\
    r"\w[bdgptclmnrv]u|er|ant|[^m]ent|eur|ai[ns]|x|it|rt|rb|rp|rd|rc|nd|ct)"

first_person_gender = [
    # être
    # a) noun
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*(une|[lstm]a|celle|[stm]on(_\w+)? [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<1f>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(étais|serais|sois|avais{_} été|aurais{_} été){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(une|[lstm]a|celle|([stm]on|un){_} "\
        rf"[aéiou]\w*[^q ][aéiou]e)(_|\b)", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(étais|serais|sois|avais{_} été|aurais{_} été){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<1m>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*(l '|[nv]otre|leur) \w+_F\b", '<1f>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*(l '|[nv]otre|leur) \w+_M\b", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(étais|serais|sois|avais{_} été|aurais{_} été){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_F\b", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(étais|serais|sois|avais{_} été|aurais{_} été){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_M\b", '<1m>'),
    # b) adjective/participle
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+[ea]s?_\w+_F\b", '<1f>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<1f>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+{suffix_fem}(_|\b)", '<1f>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+_M\b", '<1m>'),
    (rf"\b(suis|serai|ai{_} été|aurai{_} été|vais{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w*{suffix_masc}(_\w+_|\b)", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?((me{_}|m{_} ') )?(étais|serais|sois|avais{_} été|aurais{_} "\
        rf"été){_} (({adverbs} )?{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?((me{_}|m{_} ') )?(étais|serais|sois|avais{_} été|aurais{_} "\
        rf"été){_} (({adverbs} )?{negation} )?({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?((me{_}|m{_} ') )?(étais|serais|sois|avais{_} été|aurais{_} "\
        rf"été){_} (({adverbs} )?{negation} )?({adverbs} )*\w+{suffix_fem}(_|\b)", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?((me{_}|m{_} ') )?(étais|serais|sois|avais{_} été|aurais{_} "\
        rf"été){_} (({adverbs} )?{negation} )?({adverbs} )*\w+_M\b", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?((me{_}|m{_} ') )?(étais|serais|sois|avais{_} été|aurais{_} "\
        rf"été){_} (({adverbs} )?{negation} )?({adverbs} )*\w*{suffix_masc}(_\w+_|\b)", '<1m>'),
    # être, reverted forms
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[ea]s?_\w+_F\b", '<1f>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<1f>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+{suffix_fem}(_|\b)", '<1f>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+_M\b", '<1m>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w*{suffix_masc}(_\w+_|\b)", '<1m>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(une|[lstm]a|celle|[stm]on(_\w+)? [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<1f>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<1m>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_F\b", '<1f>'),
    (rf"\b(suis|étais) ?- ?je{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_M\b", '<1m>'),
    # modal with être
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(une|[lstm]a|celle|[stm]on(_\w+)? [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<1f>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<1m>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+[ea]s?_\w+_F\b", '<1f>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<1f>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+{suffix_fem}(_|\b)", '<1f>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+_M\b", '<1m>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w*{suffix_masc}(_\w+_|\b)", '<1m>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_F\b", '<1f>'),
    (rf"(je{_}|j{_} ') (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_M\b", '<1m>'),
    # devenir
    # a) noun
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(une|[lstm]a|celle|([stm]on|un){_} [aéiou]\w*"\
        rf"[^q ][aéiou]e)(_|\b)", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        "(({adverbs} )?{negation} )?({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_F\b", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_M\b", '<1m>'),
    # b) adjective/participle
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+{suffix_fem}(_|\b)", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+_M\b", '<1m>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(deviens|devenais|deviendrais?|devienne){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w*{suffix_masc}(_\w+_|\b)", '<1m>'),
    # c) composed forms
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(suis|étais|serais?|sois|ai{_} été) (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*devenue(_|\b)", '<1f>'),
    (rf"\b(je{_}|j{_} ') ((ne|n ') )?(suis|étais|serais?|sois|ai{_} été) (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*devenu(_|\b)", '<1m>'),
    # rendre
    (rf"\b(me{_}|m{_} ' (as|a|avez|ont){_}) rend\w* (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[ea]s?_\w+_F\b", '<1f>'),
    (rf"\b(me{_}|m{_} ' (as|a|avez|ont){_}) rend\w* (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+{suffix_fem}(_|\b)", '<1f>'),
    (rf"\b(me{_}|m{_} ' (as|a|avez|ont){_}) rend\w* (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<1f>'),
    (rf"\b(me{_}|m{_} ' (as|a|avez|ont){_}) rend\w* (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+_M\b", '<1m>'),
    (rf"\b(me{_}|m{_} ' (as|a|avez|ont){_}) rend\w* (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w*{suffix_masc}(_\w+_|\b)", '<1m>'),
    # avoir
    (rf"\bm{_} ' (a|as|avez|ont|avait|aviez|avaient){_} ((vous|tu|ils?|elles?){_} )?(({adverbs} )?"\
        rf"{negation} )?(été )?({adverbs} )*\w+es?_\w+_F\b(?! (que?|pourquoi|une?|[lstm]a|le?|"\
        rf"[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|"\
        rf"quelques?|plus|moins|si|beaucoup|tou[ts]|toutes?)(_|\b))", '<1f>'),
    (rf"\bm{_} ' (a|as|avez|ont|avait|aviez|avaient){_} ((vous|tu|ils?|elles?){_} )?(({adverbs} )?"\
        rf"{negation} )?(été )?({adverbs} )*\w+_M\b(?! (que?|une?|pourquoi|[lstm]a|le?|[stm]on|"\
        rf"[lstmd]es|[nv]otre|[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|"\
        rf"plus|moins|si|beaucoup|tou[ts]|toutes?)(_|\b))", '<1m>'),
    (rf"\bm{_} ' (auras|aura|aurez|auront|aurait|auriez|auraient|aies|ait|ayez|aient){_} "\
        rf"((vous|tu|ils?|elles?){_} )?(({adverbs} )?{negation} )?(été )?({adverbs} )*"\
        rf"\w+es?_\w+_F\b(?! (que?|pourquoi|une?|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|"\
        rf"[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|"\
        rf"si|beaucoup|tou[ts]|toutes?)(_|\b))", '<1f>'),
    (rf"\bm{_} ' (auras|aura|aurez|auront|aurait|auriez|auraient|aies|ait|ayez|aient){_} "\
        rf"((vous|tu|ils?|elles?){_} )?(({adverbs} )?{negation} )?(été )?({adverbs} )*"\
        rf"\w+_M\b(?! (que?|une?|pourquoi|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?|"\
        rf"ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|si|beaucoup|tou[ts]|"\
        rf"toutes?)(_|\b))", '<1m>'),
    (rf"\b(tu{_}|j{_} ') m{_} ' (avais|aurais){_} (({adverbs} )?{negation} )?(été )?({adverbs} )*"\
        rf"\w+es?_\w+_F\b(?! (que?|pourquoi|une?|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|"\
        rf"leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|si|beaucoup|"\
        rf"tou[ts]|toutes?)(_|\b))", '<1f>'),
    (rf"\b(tu{_}|j{_} ') m{_} ' (avais|aurais){_} (({adverbs} )?{negation} )?(été )?({adverbs} )*"\
        rf"\w+_M\b(?! (que?|une?|pourquoi|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?|"\
        rf"ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|si|beaucoup|tou[ts]|"\
        rf"toutes?)(_|\b))", '<1m>'),
    # other
    (r'^désolée(_|\b)', '<1f>'),
    (r'^désolé(_|\b)', '<1m>')
]

second_person_gender = [
    # être
    # a) noun
    # i) tu
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*(une|[lstm]a|celle|[stm]on(_\w+)? [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(étais|serais|sois|avais{_} été|aurais{_} été){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(une|[lstm]a|celle|([stm]on|un){_} [aéiou]"\
        rf"\w*[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(étais|serais|sois|avais{_} été|aurais{_} été){_} "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas être){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_F\b", '<2f>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas être){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_M\b", '<2m>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(étais|serais|sois|avais été|aurais été){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_F\b", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(étais|serais|sois|avais été|aurais été){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_M\b", '<2m>'),
    # ii) vous
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(une|[lstm]a|celle|[stm]on(_\w+)? [aéiou]\w*"\
        rf"[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(l '|[nv]otre|leur|des|les) \w+_F\b", '<2f>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(l '|[nv]otre|leur|des|les) \w+_M\b", '<2m>'),
    # b) adjective/participle
    # i) tu
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+{suffix_fem}(_|\b)", '<2f>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+_M\b", '<2m>'),
    (rf"\b(es|seras|as{_} été|auras{_} été|vas{_} être){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w*{suffix_masc}(_\w+_|\b)", '<2m>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?((te{_}|t{_} ') )?(étais|serais|sois|avais été|aurais été) "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?((te{_}|t{_} ') )?(étais|serais|sois|avais été|aurais été) "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?((te{_}|t{_} ') )?(étais|serais|sois|avais été|aurais été) "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+{suffix_fem}(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?((te{_}|t{_} ') )?(étais|serais|sois|avais été|aurais été) "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*\w+_M\b", '<2m>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?((te{_}|t{_} ') )?(étais|serais|sois|avais été|aurais été) "\
        rf"(({adverbs} )?{negation} )?({adverbs} )*{suffix_masc}(_\w+_|\b)", '<2m>'),
    # ii) vous
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+_M\b", '<2m>'),
    (rf"\b(êtes|étiez|avi?ez{_} été|aurez{_} été|allez{_} être|seri?ez|soyez){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    # être, reverted forms
    # a) tu
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)",
        '<2f>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*\w+{suffix_fem}(_|\b)",
        '<2f>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*\w+_M\b", '<2m>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*\w*{suffix_masc}(_\w+_|\b)",
        '<2m>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(une|[lstm]a|celle|([stm]on|un){_} [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_F\b", '<2f>'),
    (rf"\b(es|étais) ?- ?tu{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur) \w+_M\b", '<2m>'),
    # b) vous
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+_M\b", '<2m>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(une|[lstm]a|celle|([stm]on|un){_} [aéiou]\w*[^q ][aéiou][ea])s?(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur|des|les) \w+_F\b", '<2f>'),
    (rf"\b(êtes|étiez) ?- ?vous{_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur|des|les) \w+_M\b", '<2m>'),
    # modal with être
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(une|[lstm]a|celle|[stm]on(_\w+)? [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w+_M\b", '<2m>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(l '|[nv]otre|leur|des|les) \w+_F\b", '<2f>'),
    (rf"(tu{_}|t{_} '|vous{_}) (ne )?\w+ (({adverbs} )?{negation} )?être ({adverbs} )*"\
        rf"(l '|[nv]otre|leur|des|les) \w+_M\b", '<2m>'),
    # devenir
    # a) noun
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(une|[lstm]a|celle|([stm]on|un){_} [aéiou]\w*"\
        rf"[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_F\b", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*(l '|[nv]otre|leur) \w+_M\b", '<2m>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(une|[lstm]a|celle|([stm]on|un){_} [aéiou]\w*[^q ][aéiou]e)(_|\b)", '<2f>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur|des|les) \w+_F\b", '<2f>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(l '|[nv]otre|leur|des|les) \w+_M\b", '<2m>'),
    # b) adjective/participle
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w+_M\b", '<2m>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(deviens|devenais|deviendrai?s|deviennes){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+_M\b", '<2m>'),
    (rf"\b(deveni?ez|deviendri?ez|deveniez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    # c) composed forms
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(es|étais|serai?s|sois|as{_} été){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*devenue(_|\b)", '<2f>'),
    (rf"\b(tu{_}|t{_} ') ((ne|n ') )?(es|étais|serai?s|sois|as{_} été){_} (({adverbs} )?"\
        rf"{negation} )?({adverbs} )*devenu(_|\b)", '<2m>'),
    (rf"\b(êtes|étiez|seri?ez|soyez|avez{_} été){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*devenues?(_|\b)", '<2f>'),
    (rf"\b(êtes|étiez|seri?ez|soyez|avez{_} été){_} (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*devenus?(_|\b)", '<2m>'),
    # imperative with être
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*\w+_M\b", '<2m>'),
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(une|[lstm]a|celle|([stm]on|un){_} [aéiou]\w*[^q ][aéiou][ea])s?(_|\b)", '<2f>'),
    (rf"(?<!je )(sois|soyez){_} (({adverbs} )?{negation} )?({adverbs} )*"\
        rf"(un|le|celui|[stm]on)(_|\b)", '<2m>'),
    # rendre
    (rf"\b(te|t{_} '|vous){_} ((ai|a|avons|ont){_} )?rend\w* (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+[ea]s?_\w+_F\b", '<2f>'),
    (rf"\b(te|t{_} '|vous){_} ((ai|a|avons|ont){_} )?rend\w* (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+[^q ][aéiou][ea]s?(_|\b)", '<2f>'),
    (rf"\b(te|t{_} '|vous){_} ((ai|a|avons|ont){_} )?rend\w* (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+{suffix_fem}s?(_|\b)", '<2f>'),
    (rf"\b(te|t{_} '|vous){_} ((ai|a|avons|ont){_} )?rend\w* (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w+_M\b", '<2m>'),
    (rf"\b(te|t{_} '|vous){_} ((ai|a|avons|ont){_} )?rend\w* (({adverbs} )?{negation} )?"\
        rf"({adverbs} )*\w*{suffix_masc}s?(_\w+_|\b)", '<2m>'),
    # avoir
    (rf"\b(t{_} '|vous){_} (a|ai|avons|ont|avait|avions|avaient){_} ((je|nous|ils?|elles?){_} )?"\
        rf"(({adverbs} )?{negation} )?(été )?({adverbs} )*\w+es?_\w+_F\b(?! (que?|pourquoi|une?|"\
        rf"[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|"\
        rf"plusieurs|quelques?|plus|moins|si|beaucoup|tou[ts]|toutes?)(_|\b))", '<2f>'),
    (rf"\b(t{_} '|vous){_} (a|ai|avons|ont|avait|avions|avaient){_} ((je|nous|ils?|elles?){_} )?"\
        rf"(({adverbs} )?{negation} )?(été )?({adverbs} )*\w+_M\b(?! (que?|une?|pourquoi|[lstm]a|"\
        rf"le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|"\
        rf"quelques?|plus|moins|si|beaucoup|tou[ts]|toutes?)(_|\b))", '<2m>'),
    (rf"\b(t{_} '|vous){_} (aurai|aura|aurons|auront|aurait|aurions|auraient|aie|ait|ayons|aient)"\
        rf"{_} ((je|nous|ils?|elles?){_} )?(({adverbs} )?{negation} )?(été )?({adverbs} )*"\
        rf"\w+es?_\w+_F\b(?! (que?|pourquoi|une?|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|"\
        rf"leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|si|beaucoup|"\
        rf"tou[ts]|toutes?)(_|\b))", '<2f>'),
    (rf"\b(t{_} '|vous){_} (aurai|aura|aurons|auront|aurait|aurions|auraient|aie|ait|ayons|aient)"\
        rf"{_} ((je|nous|ils?|elles?){_} )?(({adverbs} )?{negation} )?(été )?({adverbs} )*\w+_M\b"\
        rf"(?! (que?|une?|pourquoi|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|[nv]os|leurs?|ces?|"\
        rf"cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|si|beaucoup|tou[ts]|toutes?)"\
        rf"(_|\b))", '<2m>'),
    (rf"\b(je{_}|j{_} ') (t{_} '|vous){_} (avais|aurais){_} (({adverbs} )?{negation} )?(été )?"\
        rf"({adverbs} )*\w+es?_\w+_F\b(?! (que?|pourquoi|une?|[lstm]a|le?|[stm]on|[lstmd]es|"\
        rf"[nv]otre|[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|"\
        rf"moins|si|beaucoup|tou[ts]|toutes?)(_|\b))", '<2f>'),
    (rf"\b(je{_}|j{_} ') (t{_} '|vous){_} (avais|aurais){_} (({adverbs} )?{negation} )?(été )?"\
        rf"({adverbs} )*\w+_M\b(?! (que?|une?|pourquoi|[lstm]a|le?|[stm]on|[lstmd]es|[nv]otre|"\
        rf"[nv]os|leurs?|ces?|cettes?|celui|celles?|ceux|plusieurs|quelques?|plus|moins|si|"\
        rf"beaucoup|tou[ts]|toutes?)(_|\b))", '<2m>'),
    # address
    (r"\bchérie(_|\b)", '<2f>'),
    (r"\bchéri(_|\b)", '<2m>'),
    (r",( (ma|mon)(_\w+)?)? (chère|amie)(_|\b)", '<2f>'),
    (r",( mon(_\w+)?)? (cher|ami)(_|\b)", '<2m>')
]

politeness_level = [
    # singular pronouns
    (r"\b(toi|tu|te|ton|ta|tes|tien|tienne|tiennes)(_|\b)", '<T>'),
    (r"\bt(_\w+)? ' ", '<T>'),
    (r"\bles\w+ tiens(_|\b)", '<T>'),
    # plural pronouns
    (r'\b(vous|votre|vos|vôtre|vôtres)(_|\b)', '<V>'),
    # imperative
    (r'(VERB|AUX)_Imp_Sing', '<T>'),
    (r'(VERB|AUX)_Imp_Plur', '<V>'),
    (r'(?<!\bass)(ez|dites|faites)(_|\b)', '<V>'),
    # explicit list of singular imperatives
    (r'^(ne )?(réponds|regarde|dis|donne|demande|prend(s)|dors|mange|bois|[ée]coute|ferme|ouvre|'\
        r'arrête|tiens|mets|promets|va|viens|laisse|fais|touche|écris)(_|\b)', '<T>'),
    # imperative singular
    (r"^ne ((me|m '|te|t '|lui|leur|le|la|les|nous) )?"\
        r"(?!(\w+ez|\w+ons|pas|jamais|plus|faites|dites)(_|\b))", '<T>'),
    (r'(?<=\w\w)(?<!(\wez|ons|tes)) ?- ?(moi|toi|lui|leur|les)(_|\b)', '<T>')
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
        mood_orig = token.morph.get('Mood')
        number = token.morph.get('Number')
        if mood_orig == []:
            mood = ''
        else:
            if number != []:
                mood = '_' + mood_orig[0] + '_' + number[0] if mood_orig[0] == 'Imp' else ''
            else:
                mood = '_' + mood_orig[0] if mood_orig[0] == 'Imp' else ''
        if gender == []:
            if mood == '':
                tokens.append(f'{token.text}')
            else:
                tokens.append(f'{token.text}_{token.tag_}{mood}')
        else:
            tokens.append(f'{token.text}_{token.tag_}_{gender[0][0]}')
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
