from typing import Optional

from spacy.tokens import Doc, Span

from lib.nlp.nlp_processor import NLPProcessor

_locations = {'micronesia', 'poland', 'philippines', 'portugal', 'anguilla', 'niue', 'moldova', 'bermuda', 'canada',
              'tonga', 'aruba', 'angola', 'ireland', 'ecuador', 'timor', 'afghanistan', 'iraq', 'european union',
              'hong kong', 'liechtenstein', 'maldives', 'palau', 'benin', 'syria', 'guatemala', 'venezuela', 'armenia',
              'tokelau', 'turkmenistan', 'tuvalu', 'congo', 'azerbaijan', 'bosnia and herzegovina', 'madagascar',
              'bhutan', 'burundi', 'cameroon', 'bangladesh', 'ukraine', 'qatar', 'ethiopia', 'jordan', 'uruguay',
              'brunei', 'papua new guinea', 'haiti', 'fiji', 'united states', 'central african republic', 'senegal',
              'cook islands', 'slovenia', 'suriname', 'iran', 'greece', 'saint helena', 'denmark', 'ghana', 'belgium',
              'albania', 'bahamas', 'lesotho', 'cambodia', 'guernsey', 'kyrgyzstan', 'germany', 'wales', 'samoa',
              'bulgaria', 'finland', 'israel', 'sint maarten', 'malaysia', 'thailand', 'macao', 'estonia', 'guyana',
              'rwanda', 'algeria', 'northern cyprus', 'france', 'pakistan', 'mali', 'belize', 'taiwan',
              'northern ireland', 'croatia', 'indonesia', 'africa', 'georgia', 'uzbekistan', 'liberia', 'guineabissau',
              'lithuania', 'uganda', 'slovakia', 'equatorial guinea', 'belarus', 'andorra', 'luxembourg', 'malawi',
              'spain', 'oman', 'gambia', 'wallis and futuna', 'honduras', 'jersey', 'congo', 'netherlands', 'latvia',
              'togo', 'montenegro', 'kuwait', 'burkina faso', 'south africa', 'serbia', 'gibraltar', 'guinea',
              'singapore', 'japan', 'nauru', 'cote divoire', 'kiribati', 'isle of man', 'sao tome and principe',
              'comoros', 'malta', 'vanuatu', 'saint vincent and the grenadines', 'united kingdom', 'russia', 'dominica',
              'egypt', 'french polynesia', 'brazil', 'grenada', 'south sudan', 'argentina', 'somalia', 'sri lanka',
              'tanzania', 'kosovo', 'new zealand', 'india', 'bonaire sint eustatius and saba', 'iceland', 'nigeria',
              'seychelles', 'mozambique', 'vietnam', 'hungary', 'niger', 'chad', 'austria', 'greenland', 'kenya',
              'barbados', 'panama', 'saudi arabia', 'yemen', 'djibouti', 'vatican', 'sudan', 'palestine', 'tajikistan',
              'mauritius', 'gabon', 'oceania', 'chile', 'cape verde', 'asia', 'italy', 'mexico', 'paraguay',
              'antigua and barbuda', 'montserrat', 'cyprus', 'botswana', 'pitcairn', 'laos', 'tunisia', 'switzerland',
              'trinidad and tobago', 'china', 'saint pierre and miquelon', 'north macedonia', 'zimbabwe', 'kazakhstan',
              'morocco', 'faeroe islands', 'namibia', 'norway', 'europe', 'jamaica', 'scotland', 'eritrea', 'lebanon',
              'bahrain', 'czechia', 'cuba', 'nicaragua', 'monaco', 'peru', 'libya', 'solomon islands', 'romania',
              'san marino', 'nepal', 'falkland islands', 'south america', 'sweden', 'el salvador', 'england',
              'colombia', 'australia', 'north america', 'mongolia', 'south korea', 'saint lucia',
              'united arab emirates', 'turkey', 'marshall islands', 'british virgin islands', 'dominican republic',
              'turks and caicos islands', 'new caledonia', 'mauritania', 'bolivia', 'sierra leone', 'costa rica',
              'curacao', 'eswatini', 'saint kitts and nevis', 'cayman islands', 'myanmar', 'zambia'}


class LocationRecognizer:
    def __init__(self):
        self._nlp_processor = NLPProcessor()

    def recognize_location(self, span: Span) -> Optional[str]:
        location_ents = [ent.text for ent in span.ents
                         if ent.label_ == "GPE"]
        if len(location_ents) == 0:
            # If automated entity recognition doesn't work, try a manual approach

            for token in span:
                normalized_token = self._nlp_processor.normalize_country_name(token.text)

                if normalized_token in _locations:
                    return token.text

            return None
        else:
            return location_ents[0]
