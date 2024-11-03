#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MAX 128

struct stog {
	char operacija;
	double broj;
	struct stog* next;
};

int push(struct stog*, char, double);
int pop(struct stog*);
char peekC(static struct stog*);
double peekD(static struct stog*);
int vaznost(char);
int turntonum(char);
char turntochar(int);
char* removeWhiteSpace(char*);
char* InfixToPostfix(char*);
double CalculatePostfix(char*);

int main() {
	char* buffer=NULL;
	char* pfix = NULL;
	buffer = (char*)malloc(MAX * sizeof(char));
	printf("Unesi operaciju: "); 
	fgets(buffer, MAX, stdin);

	//ASCII 48 = 0  -  57 = 9

	pfix = InfixToPostfix(buffer); //Sigma
	printf("%s\n", pfix);
	printf("=%lf", CalculatePostfix(pfix));

	return 0;
}

int push(struct stog* head, char operacija, double broj) {
	struct stog* temp = NULL;
	temp = (struct stog*)malloc(sizeof(struct stog));
	if (temp == NULL) {
		printf("Failed to allocate memory...\n");
		return EXIT_FAILURE;
	}
	temp->operacija = operacija;
	temp->broj = broj;
	temp->next = head->next;
	head->next = temp;
	return EXIT_SUCCESS;
}

int pop(struct stog* head) {
	if (head->next == NULL) {
		printf("No elements to remove...\n");
		return EXIT_FAILURE;
	}
	struct stog* temp=head->next;
	head->next = temp->next;
	free(temp);
	return EXIT_SUCCESS;
}

char peekC(static struct stog* head) {
	if (head->next == NULL) {
		return '\0';
	}
	else {
		return head->next->operacija;
	}
}

double peekD(static struct stog* head) {
	if (head->next == NULL) {
		return 0;
	}
	else {
		return head->next->broj;
	}
}

int vaznost(char c) {
	if (c == '^') {
		return 3;
	}
	if (c == '/' || c == '*') {
		return 2;
	}
	else if (c == '+' || c == '-') {
		return 1;
	}
	else {
		return 0;
	}
}

int turntonum(char c) {
	return c - 48;
}

char turntochar(int n) {
	return n + 48;
}

char* removeWhiteSpace(char* buffer) {
	if (buffer == NULL) {
		return NULL;
	}
	int i = 0;
	int j;
	int n=0;
	while (buffer[i] != '\0') {
		n++;
		i++;
	}
	n++;
	i = 0;
	while (buffer[i] != '\0') {
		if (buffer[i] == ' '||buffer[i]=='\n') {
			j = i;
			while (buffer[j+1] != '\0') {
				buffer[j] = buffer[j + 1];
				j++;
			}
			buffer[j] = buffer[j+1];
			n--;
			buffer = (char*)realloc(buffer,n * sizeof(char));
			if (buffer == NULL) {
				return NULL;
			}
		}
		if (buffer[i] == ' ') {
			continue;
		}
		else {
			i++;
		}
	}
	return buffer;
}

char* InfixToPostfix(char* buffer) {
	buffer=removeWhiteSpace(buffer);
	struct stog* head = NULL;
	head = (struct stog*)malloc(sizeof(struct stog));
	if (head == NULL) {
		return NULL;
	}
	head->next = NULL;
	if (buffer == NULL) {
		return NULL;
	}
	char* rBuffer = NULL;
	int i=0,n=0;
	while (1) {
		if ((buffer[i] >= 48 && buffer[i] <= 57)||buffer[i]=='.') {
			while ((buffer[i] >= 48 && buffer[i] <= 57)||buffer[i]=='.') {
				rBuffer = (char*)realloc(rBuffer, ((n + 1) * sizeof(char)));
				if (rBuffer == NULL) {
					return NULL;
				}
				rBuffer[n] = buffer[i];
				n++;
				i++;
			}
			rBuffer = (char*)realloc(rBuffer, ((n + 1) * sizeof(char)));
			if (rBuffer == NULL) {
				return NULL;
			}
			rBuffer[n] = ' ';
			n++;
		}
		else {
			if (peekC(head) == '\0') {
				push(head,buffer[i],0);
				i++;
			}

			else if (buffer[i] == '(') {
				push(head, buffer[i],0);
				i++;
			}

			else if (buffer[i] == ')') {
				while (peekC(head) != '(') {
					rBuffer = (char*)realloc(rBuffer, ((n + 1) * sizeof(char)));
					if (rBuffer == NULL) {
						return NULL;
					}
					rBuffer[n] = peekC(head);
					pop(head);
					n++;
				}
				pop(head);
				i++;

			}
			
			else if (vaznost(buffer[i])>vaznost(peekC(head))) {
				push(head,buffer[i],0);
				i++;
			}
			else {
				while (vaznost(buffer[i]) <= vaznost(peekC(head))) {
					rBuffer = (char*)realloc(rBuffer, ((n + 1) * sizeof(char)));
					if (rBuffer == NULL) {
						return NULL;
					}
					rBuffer[n] = peekC(head);
					pop(head);
					n++;
				}
				push(head, buffer[i],0);
				i++;
			}

		}
		if (buffer[i] == '\0') {
			while (peekC(head) != '\0') {
				rBuffer = (char*)realloc(rBuffer, ((n + 1) * sizeof(char)));
				if (rBuffer == NULL) {
					return NULL;
				}
				rBuffer[n] = peekC(head);
				pop(head);
				n++;
			}
			break;
		}
	}
	rBuffer = (char*)realloc(rBuffer, ((n + 1) * sizeof(char)));
	if (rBuffer == NULL) {
		return NULL;
	}
	rBuffer[n] = '\0';
	n++;
	free(head);
	return rBuffer;
}

double CalculatePostfix(char* pfix) {
	struct stog* head = NULL;
	head = (struct stog*)malloc(sizeof(struct stog));
	if (head == NULL) {
		return NULL;
	}
	head->next = NULL;
	if (pfix == NULL) {
		return EXIT_FAILURE;
	}
	int i = 0;
	double prec=0;
	double nprec = -1;
	double temp1;
	double temp2;
	double temp3;
	while (pfix[i] != '\0') {
		if ((pfix[i] >= 48 && pfix[i] <= 57)||pfix[i]=='.') {
			while (pfix[i] != ' ') {
				if (prec == 0 && pfix[i]!='.') {
					prec = (double)turntonum(pfix[i]);
				}
				else if (pfix[i]=='.') {
					i++;
					if (pfix[i] < 48 || pfix[i]>57) {
						break;
					}
					while (pfix[i] != ' ') {
						prec = prec + (double)turntonum(pfix[i]) * pow(10, nprec);
						nprec--;
						i++;
					}
					i--;
				}
				else {
					prec = prec * 10 + (double)turntonum(pfix[i]);
				}
				i++;
			}
			i++;
			push(head, '\0', prec);
			nprec = -1;
			prec = 0;
		}
		else if (pfix[i] == '+') {
			temp2 = peekD(head);
			pop(head);
			temp1 = peekD(head);
			pop(head);
			push(head, '\0',temp1 + temp2);
			i++;
		}
		else if (pfix[i] == '*') {
			temp2 = peekD(head);
			pop(head);
			temp1 = peekD(head);
			pop(head);
			push(head, '\0',temp1 * temp2);
			i++;
		}
		else if (pfix[i] == '-') {
			temp2 = peekD(head);
			pop(head);
			temp1 = peekD(head);
			pop(head);
			push(head, '\0',temp1 - temp2);
			i++;
		}
		else if (pfix[i] == '^') {
			temp2 = peekD(head);
			pop(head);
			temp1 = peekD(head);
			pop(head);
			push(head, '\0',pow(temp1, temp2));
			i++;
		}
		else if (pfix[i] == '/') {
			temp2 = peekD(head);
			pop(head);
			temp1 = peekD(head);
			pop(head);
			push(head, '\0', temp1/temp2);
			i++;
		}
		
	}
	temp3 = peekD(head);
	pop(head);
	free(head);
	return temp3;
}