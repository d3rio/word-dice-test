This is a simple python script that lets you test the words in a book for the mental 6-sided die method explained
here: https://boingboing.net/2020/04/10/how-to-roll-an-imaginary-6-sid.html.

The basic method is the following:
1. Pick a random word
2. Encode each letter as a number: a=1, b=2, etc.
3. Add up the numbers of the word to get a single number N.
4. Divide that number by 9 and keep the remainder.  This is equivalent to the N%9 or mod(N,9) function.
5. If your remainder is 6, 7, or 8, then discard it.
6. Add +1 to your number to get a final dice roll value.

The alternate method is to divide by 6 instead of 9.  This negates the need to discard any numbers.

This script does the calculations above for every word in a book downloaded from Project Gutenberg.  It also filters out
repeat words so that each word is used no more than once.