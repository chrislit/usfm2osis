# -*- coding: utf-8 -*-
"""usfm2osis.data

Copyright 2012-2015 by Christopher C. Little

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full text of the GNU General Public License is available at:
<http://www.gnu.org/licenses/gpl-3.0.txt>.
"""

from __future__ import unicode_literals

bookDict = {
    ### Known USFM Book codes from Paratext
    ### Cf. http://ubs-icap.org/chm/usfm/2.35/index.html?book_codes.htm
    # OT
    'GEN':'Gen', 'EXO':'Exod', 'LEV':'Lev', 'NUM':'Num', 'DEU':'Deut',
    'JOS':'Josh', 'JDG':'Judg', 'RUT':'Ruth', '1SA':'1Sam', '2SA':'2Sam',
    '1KI':'1Kgs', '2KI':'2Kgs', '1CH':'1Chr', '2CH':'2Chr', 'EZR':'Ezra',
    'NEH':'Neh', 'EST':'Esth', 'JOB':'Job', 'PSA':'Ps', 'PRO':'Prov',
    'ECC':'Eccl', 'SNG':'Song', 'ISA':'Isa', 'JER':'Jer', 'LAM':'Lam',
    'EZK':'Ezek', 'DAN':'Dan', 'HOS':'Hos', 'JOL':'Joel', 'AMO':'Amos',
    'OBA':'Obad', 'JON':'Jonah', 'MIC':'Mic', 'NAM':'Nah', 'HAB':'Hab',
    'ZEP':'Zeph', 'HAG':'Hag', 'ZEC':'Zech', 'MAL':'Mal',
    # NT
    'MAT':'Matt', 'MRK':'Mark', 'LUK':'Luke', 'JHN':'John', 'ACT':'Acts',
    'ROM':'Rom', '1CO':'1Cor', '2CO':'2Cor', 'GAL':'Gal', 'EPH':'Eph',
    'PHP':'Phil', 'COL':'Col', '1TH':'1Thess', '2TH':'2Thess', '1TI':'1Tim',
    '2TI':'2Tim', 'TIT':'Titus', 'PHM':'Phlm', 'HEB':'Heb', 'JAS':'Jas',
    '1PE':'1Pet', '2PE':'2Pet', '1JN':'1John', '2JN':'2John', '3JN':'3John',
    'JUD':'Jude', 'REV':'Rev',
    # DC - Catholic
    'TOB':'Tob', 'JDT':'Jdt', 'ESG':'EsthGr', 'WIS':'Wis', 'SIR':'Sir',
    'BAR':'Bar', 'LJE':'EpJer', 'S3Y':'PrAzar', 'SUS':'Sus', 'BEL':'Bel',
    '1MA':'1Macc', '2MA':'2Macc',
    # DC - Eastern Orthodox
    '3MA':'3Macc', '4MA':'4Macc', '1ES':'1Esd', '2ES':'2Esd', 'MAN':'PrMan',
    'PS2':'AddPs',
    # Rahlfs' LXX
    'ODA':'Odes', 'PSS':'PssSol',
    # Esdrae
    'EZA':'4Ezra', '5EZ':'5Ezra', '6EZ':'6Ezra',
    # Inconsistency with Esther
    'DAG':'DanGr',
    # Syriac
    'PS3':'5ApocSyrPss', '2BA':'2Bar', 'LBA':'EpBar',
    # Ethiopic
    'JUB':'Jub', 'ENO':'1En', '1MQ':'1Meq', '2MQ':'2Meq', '3MQ':'3Meq',
    'REP':'Reproof', '4BA':'4Bar',
    # Vulgate
    'LAO':'EpLao',

    # Additional non-biblical books
    'XXA':'XXA', 'XXB':'XXB', 'XXC':'XXC', 'XXD':'XXD', 'XXE':'XXE',
    'XXF':'XXF', 'XXG':'XXG',

    # Peripheral books
    'FRT':'FRONT', 'INT':'INTRODUCTION', 'BAK':'BACK', 'CNC':'CONCORDANCE',
    'GLO':'GLOSSARY', 'TDX':'INDEX', 'NDX':'GAZETTEER', 'OTH':'X-OTHER'
    }

addBookDict = {
    ### Deprecated
    # Rahlfs
    'JSA':'JoshA', 'JDB':'JudgB', 'TBS':'TobS', 'SST':'SusTh', 'DNT':'DanTh',
    'BLT':'BelTh',
    # Esdrae
    '4ES':'4Ezra', '5ES':'5Ezra', '6ES':'6Ezra',


    ### Proposed Additions:
    # <http://lc.bfbs.org.uk/e107_files/downloads/canonicalissuesinparatext.pdf>
    # Alternate Psalms
    'PSB':'PsMet',
    # Vulgate
    'PSO':'PrSol', 'PJE':'PrJer',
    # Armenian
    'WSI':'WSir', 'COP':'EpCorPaul', '3CO':'3Cor', 'EUT':'PrEuth',
    'DOJ':'DormJohn',
    # Apostolic Fathers
    '1CL':'1Clem', '2CL':'2Clem', 'SHE':'Herm', 'LBA':'Barn', 'DID':'Did',
    ###
    # Proposed replacements:
    # <http://lc.bfbs.org.uk/e107_files/downloads/canonicalissuesinparatext.pdf>
    'ODE':'Odes',

    # Additional biblical books
    'ADE':'AddEsth'
    }


canonicalOrder = [
    # General principles of ordering:
    # 1) Protocanonical books follow standard Protestant order within OT & NT
    # 2) Intertestamentals follow the OT
    # 3) NT-Apocrypha follow the NT
    # 4) Apostolic Fathers follow NT-deuterocanonicals
    # Specific principles:
    # 1) Book representing parts of protocanonical books follow the primary book
    # 2) Variants follow primary forms
    # 3) Books that appear in only one tradition or Bible appear following their
    #    traditional/attested antecedent

    # There's no fool-proof way to order books without knowing the tradition
    # ahead of time, but this ordering should get it right often for many common
    # real Bibles.

    # Front Matter
    'FRONT', 'INTRODUCTION',

    # OT
    'Gen', 'Exod', 'Lev', 'Num', 'Deut', 'Josh', 'JoshA', 'Judg', 'JudgB',
    'Ruth', '1Sam', '2Sam', '1Kgs', '2Kgs', '1Chr', '2Chr', 'PrMan', 'Jub',
    '1En', 'Ezra', 'Neh', 'Tob', 'TobS', 'Jdt', 'Esth', 'EsthGr', 'AddEsth',
    '1Meq', '2Meq', '3Meq', 'Job', 'Ps', 'AddPs', '5ApocSyrPss', 'PsMet',
    'Odes', 'Prov', 'Reproof', 'Eccl', 'Song', 'Wis', 'Sir', 'WSir', 'PrSol',
    'PssSol', 'Isa', 'Jer', 'Lam', 'PrJer', 'Bar', 'EpJer', '2Bar', 'EpBar',
    '4Bar', 'Ezek', 'Dan', 'DanGr', 'DanTh', 'PrAzar', 'Sus', 'SusTh', 'Bel',
    'BelTh', 'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab',
    'Zeph', 'Hag', 'Zech', 'Mal',

    # Intertestamentals
    '1Esd', '2Esd', '4Ezra', '5Ezra', '6Ezra', '1Macc', '2Macc', '3Macc',
    '4Macc',

    # NT
    'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph',
    'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Heb',
    'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev',
    # NT-Apocrypha
    'EpLao', 'EpCorPaul', '3Cor', 'PrEuth', 'DormJohn',
    # AF
    '1Clem', '2Clem', 'Herm', 'Barn', 'Did',

    # Private-Use Extensions
    'XXA', 'XXB', 'XXC', 'XXD', 'XXE', 'XXF', 'XXG',

    # Back Matter
    'BACK', 'CONCORDANCE', 'GLOSSARY', 'INDEX', 'GAZETTEER', 'X-OTHER'
    ]

usfmNumericOrder = [
    # Front Matter
    'FRONT', 'INTRODUCTION',

    # OT 01-39
    'Gen', 'Exod', 'Lev', 'Num', 'Deut', 'Josh', 'Judg', 'Ruth', '1Sam', '2Sam',
    '1Kgs', '2Kgs', '1Chr', '2Chr', 'Ezra', 'Neh', 'Esth', 'Job', 'Ps', 'Prov',
    'Eccl', 'Song', 'Isa', 'Jer', 'Lam', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos',
    'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal',

    # NT 41-67
    'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph',
    'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Heb',
    'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev',

    # Apocrypha 68-87 (plus AddEsth, inserted after EsthGr)
    'Tob', 'Jdt', 'EsthGr', 'AddEsth', 'Wis', 'Sir', 'Bar', 'EpJer', 'PrAzar',
    'Sus', 'Bel', '1Macc', '2Macc', '3Macc', '4Macc', '1Esd', '2Esd', 'PrMan',
    'AddPs', 'Odes', 'PssSol',

    # Esdrae A4-A6
    '4Ezra', '5Ezra', '6Ezra',

    # Gk. Daniel, Syriac additions, Ethiopic additions, Laodiceans B2-C2
    'DanGr', '5ApocSyrPss', '2Bar', 'EpBar', 'Jub', '1En', '1Meq', '2Meq',
    '3Meq', 'Reproof', '4Bar', 'EpLao',

    # Books not currently adopted into USFM, in order given by BFBS
    # Metrical Psalms
    'PsMet',
    # Vulgate
    'PrSol', 'PrJer',
    # Armenian
    'WSir', 'EpCorPaul', '3Cor', 'PrEuth', 'DormJohn',
    # NT Codices
    '1Clem', '2Clem', 'Herm', 'Barn', 'Did',

    # Books not currently adopted into USFM, recommended for removal by BFBS
    'JoshA', 'JudgB', 'TobS', 'DanTh', 'SusTh', 'BelTh',

    # Private-Use Extensions
    'XXA', 'XXB', 'XXC', 'XXD', 'XXE', 'XXF', 'XXG',

    # Back Matter
    'BACK', 'CONCORDANCE', 'GLOSSARY', 'INDEX', 'GAZETTEER', 'X-OTHER'
    ]

specialBooks = ['FRONT', 'INTRODUCTION', 'BACK', 'CONCORDANCE', 'GLOSSARY',
                'INDEX', 'GAZETTEER', 'X-OTHER']

peripherals = {
    'Title Page':'titlePage', 'Half Title Page':'x-halfTitlePage',
    'Promotional Page':'x-promotionalPage', 'Imprimatur':'imprimatur',
    'Publication Data':'publicationData', 'Foreword':'x-foreword',
    'Preface':'preface', 'Table of Contents':'tableofContents',
    'Alphabetical Contents':'x-alphabeticalContents',
    'Table of Abbreviations':'x-tableofAbbreviations',
    'Chronology':'x-chronology', 'Weights and Measures':'x-weightsandMeasures',
    'Map Index':'x-mapIndex', 'NT Quotes from LXX':'x-ntQuotesfromLXX',
    'Cover':'coverPage', 'Spine':'x-spine'
    }

introPeripherals = {
    'Bible Introduction':'bible', 'Old Testament Introduction':'oldTestament',
    'Pentateuch Introduction':'pentateuch', 'History Introduction':'history',
    'Poetry Introduction':'poetry', 'Prophecy Introduction':'prophecy',
    'New Testament Introduction':'newTestament',
    'Gospels Introduction':'gospels', 'Acts Introduction':'acts',
    'Epistles Introduction':'epistles', 'Letters Introduction':'letters',
    'Deuterocanon Introduction':'deuterocanon'
    }

filename2osis = dict()
