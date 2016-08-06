#include<stdio.h>
#include<stdlib.h>

//C 单链表

struct node {
   int val;
   struct node *next;
}; 

struct node* BuildOneTwoThree(void);
int Length(struct node* head);

int main(void) {
    int len;
    struct node* head = BuildOneTwoThree();
    len = Length(head); 
    printf("list length is %d\n", len);

    return 0;
}

struct node* BuildOneTwoThree(void) {
    struct node* one = NULL;
    struct node* two = NULL;
    struct node* three = NULL;

    one = malloc(sizeof(struct node));
    two = malloc(sizeof(struct node));
    three = malloc(sizeof(struct node));

    one->val = 1;
    one->next = two;

    two->val = 2;
    two->next = three;

    three->val = 3;
    three->next = NULL;
       
    return one;
}

int Length(struct node* head) {
    struct node* curr = head;
    int count = 0;

    while (curr != NULL) {
        count++;
        curr = curr->next;
    }

    return count;
}
