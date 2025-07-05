def permute(s, answer):
    if len(s) == 0:

        # Return value jika valuenya sudah batas akhir
        print(answer)
        return
    for i in range(len(s)):
        ch = s[i]
        left_substr = s[:i]
        right_substr = s[i+1:]
        rest = left_substr + right_substr
        # Recursive, call fungsi itu sendiri
        permute(rest, answer + ch)

# POC
permute('abc','')
'''
# Output
abc
acb
bac
bca
cab
cba
'''

def plagiarism_check(pattern_doc, text_doc):
    segments = [pattern_doc[i:i+20] for i in range(0, len(pattern_doc), 20)]
    match_count = 0
    for seg in segments:
        if seg in text_doc:
            match_count += 1
    return (match_count / len(segments)) * 100

# POC
print(plagiarism_check('Unpam Paling Oke','Unpam Paling Oke di Indonesia raya'))
'''
# Output
100.0
'''
