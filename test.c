#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <conio.h>

#define SIZE 4

int board[SIZE][SIZE];

void print() {
    system("cls");
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("+----");
        }
        printf("+\n");
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == 0) {
                printf("|    ");
            } else {
                printf("|%4d", board[i][j]);
            }
        }
        printf("|\n");
    }
    for (int j = 0; j < SIZE; j++) {
        printf("+----");
    }
    printf("+\n");
}

void reset() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            board[i][j] = 0;
        }
    }
}

void place() {
    int numEmptyCells = 0;
    int emptyCells[SIZE * SIZE][2];
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == 0) {
                emptyCells[numEmptyCells][0] = i;
                emptyCells[numEmptyCells][1] = j;
                numEmptyCells++;
            }
        }
    }
    if (numEmptyCells > 0) {
        int randomIndex = rand() % numEmptyCells;
        int x = emptyCells[randomIndex][0];
        int y = emptyCells[randomIndex][1];
        board[x][y] = (rand() % 2 + 1) * 2; // place 2 or 4
    }
}

void rotate(int count) {
    int temp[SIZE][SIZE];
    for (int k = 0; k < count; k++) {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                temp[i][j] = board[i][j];
            }
        }
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = temp[SIZE - 1 - j][i];
            }
        }
    }
}

int move(int direction) {
    int changed = 0;
    rotate(direction);
    for (int i = 0; i < SIZE; i++) {
        int current = 0;
        int lastMerged = -1;
        for (int j = 1; j < SIZE; j++) {
            if (board[i][j] != 0) {
                if (board[i][j] == board[i][current] && lastMerged != current) {
                    board[i][current] *= 2;
                    board[i][j] = 0;
                    lastMerged = current;
                    changed = 1;
                } else if (board[i][current] == 0) {
                    board[i][current] = board[i][j];
                    board[i][j] = 0;
                    changed = 1;
                } else if (++current && j != current) {
                    board[i][current] = board[i][j];
                    board[i][j] = 0;
                    changed = 1;
                }
            }
        }
    }
    rotate(4 - direction);
    return changed;
}

int main() {
    int ch = 0;
    srand(time(0));
    while (ch != 27) {
        ch = ch ? getch() : 63;
        if (ch == 63) {
            reset();
            place();
            place();
            print();
        } else if (ch == 224) {
            char  map[5] = {75, 80, 77, 72, 0};
            char* found = strchr(map, getch());
            if (found && move(found - map)) {
                place();
                print();
            }
        }
    }
    return 0;
}
