// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27
// 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26
// a  | b  | c  | d  | e  | f  | g  | h  | i  | j  | k  | l  | m  | n  | o  | p  | q  | r  | s  | t  | u  | v  | w  | x  | y  | z  | \'


// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

bool malloc_NODE(node *nodeName), spellChecking(const char *word, int wordPos, char cursor, node *branch),
    unloadTrie(node *branch);
int countWords(node *branch), give_letter_val(char cursor);
void initialise_node(node *ptr);

// Represents a trie
node *root;

// Position Index = how much of reserved memory in the trie is used
int dictCount = 0, nodeSize = sizeof(node);

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(nodeSize);
    if (root == NULL)
        return false;
    initialise_node(root);

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // The first letter always starts at the beginning of root
    node *branch = root;

    // Insert words into trie
    // I'm going to try reading each character and marking word end if I get to '\n'
    for (int c = fgetc(file); c != EOF; c = fgetc(file))
    {
        // If we're at a new line, we've got the end of a word
        if (c == '\n')
        {
            branch->is_word = true;
            dictCount++;
            // We've got a new word coming so we reset to the start of the trie
            branch = root;
        }
        else
        {
            // We need the value of the letter
            int letterVal = give_letter_val(c);

            // Check if the relevant child pointer is NULL
            if (branch->children[letterVal] == NULL)
            {
                // If it is, we need to malloc a new chunk of memory
                branch->children[letterVal] = malloc(nodeSize);
                if (branch->children[letterVal] == NULL)
                    return false;
                initialise_node(branch->children[letterVal]);
            }
        // Now we look at the next node
        branch = branch->children[letterVal];
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dictCount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // First we get the first letter of the word
    char cursor = word[0];

    // I smell recursion.
    return spellChecking(word, 0, cursor, root);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (root == NULL)
        return false;

    return unloadTrie(root);
}

// I use this more than once so now it's a function
// a/A = 0, z/Z = 25 and \' = 26
int give_letter_val(char cursor)
{
    return (cursor == '\'') ? 26:tolower(cursor) - 'a';
}

// Recursivley traces the trie for validation
bool spellChecking(const char *word, int wordPos, char cursor, node *branch)
{
    // We get the int value of the cursor
    int letterVal = give_letter_val(cursor);

    // We want to look ahead to see if our cursor is on the last letter of this word
    wordPos++;

    while (word[wordPos] != '\0')
    {
        // Ask if the current letter is present in the current branch
        if (branch->children[letterVal] != NULL)
            // If it is we do the same for the next letter in the next step of the path
            return spellChecking(word, (wordPos), word[wordPos], branch->children[letterVal]);

    return false;
    }

    // If this is the last letter then we want to verify this is both an existing letter
    // AND that letter is marked as a word ending.
    // This is where the recursion begins wrapping itself up.
    if (branch->children[letterVal] != NULL && branch->children[letterVal]->is_word)
        return true;
    else
        return false;
}

// Recursively unloads the trie
bool unloadTrie(node *branch)
{
    // If it doesn't exist then we can't unload it
    if (branch == NULL)
        return false;

    // Check each element of children[]
    for (int i = 0; i < N; i++)
    {
        // If it's not empty then dive in
        if (branch->children[i] != NULL)
        {
            if (!unloadTrie(branch->children[i]))
                return false;
        }
    }

    // By this point, every child should be freed or already NULL so we can free this node
    free(branch);
    return true;
}

// Don't need to repeat this chunk of code every time I malloc
void initialise_node(node *ptr)
{
    ptr->is_word = false;
    for (int i = 0; i < N; i++)
        ptr->children[i] = NULL;
}