from math import comb
message = input("Veuillez entrer la phrase à traduire : ")

def generate_translation(msg, partial_trans, translated, f):
    if len(msg) == 0:
        dict_print = ", ".join("{}->{}".format(k, v) for k, v in partial_trans.items())
        msg_print = "".join(translated)[::-1]
        f.write("{} ({})\n".format(msg_print, dict_print))
    else:
        head = msg[0]
        if head == " ":
            generate_translation(msg[1:], partial_trans, translated + [" "], f)
        elif head in partial_trans:
            generate_translation(msg[1:], partial_trans, translated + [partial_trans[head]], f)
        else:
            chars_allowed = [x for x in alphabet if x not in partial_trans.values()]
            for c in chars_allowed:
                partial_trans[head] = c
                generate_translation(msg[1:], partial_trans, translated + [c], f)
                del partial_trans[head]

with open("alphabet.txt", "r") as f:
    alphabet = f.read().splitlines()[0]

suppositions = dict()
ignored = dict()
with open("suppositions.txt", "r") as f:
    supps = f.read().splitlines()
    supps = [x.strip().split() for x in supps]
    for index, (x, y) in enumerate(supps):
        assert len(x) == 1 and len(y) == 1, "la ligne {} est mal formée".format(index + 1)
        if x in message:
            suppositions[x] = y
        else:
            ignored[x] = y

unique_letters = set(x for x in message if x != " " and x not in suppositions)
len_supps = len(suppositions)
letters_left = len(alphabet) - len_supps
all_combis = comb(letters_left, unique_letters)
if all_combis > 10000:
    answer = input("Plus de 10000 combinaisons possibles ({}). Continuer ? (oui/non)".format(all_combis)
    if answer != "oui":
        exit()


with open("result.txt", "w") as f:
    f.write("Génération de toutes les traductions de la phrase : " + message)
    f.write("\nContraintes de traduction : " + ", ".join("{}->{}".format(k, v) for k, v in suppositions.items()))
    if len(ignored) > 0:
        f.write("\nContraintes ignorées : " + ", ".join("{}->{}".format(k, v) for k, v in ignored.items()))
    f.write("\n--------------------------------------\n")
    generate_translation(message, suppositions, [], f)
print("les résultats ont été sauvegardés dans result.txt")
