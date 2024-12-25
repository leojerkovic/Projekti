#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct tranzakcija;
typedef struct tranzakcija* ptranzakcija;
typedef struct tranzakcija {
	int red;
	char vrsta[100];
	double iznos;
	ptranzakcija next;
}tranzakcija;

struct racun;
typedef struct racun* pracun;
typedef struct racun {
	char korisnickoime[15];
	char lozinka[15];
	double ustedevina;
	tranzakcija head;
	pracun next;
}racun;

struct osoba;
typedef struct osoba* posoba;
typedef struct osoba {
	char ime[10];
	char prezime[10];
	unsigned int oib;
	racun korisnickiracun;
	posoba next;
}osoba;

unsigned int OIBprovjera();
char* KImeProvjera(posoba);
char* LozinkaProvjera();
bool Banka(posoba);
int Registracija(posoba);
posoba Login(posoba);
bool Korisnik(posoba, posoba);
int Uplata(posoba);
int Isplata(posoba);
int Placanje(posoba,posoba);
int UpisPovijest(posoba, const char[], double);
int IspisPovijest(posoba);
int Brisanje(posoba, posoba);
int UpisUDatoteku(posoba);
int IspisIzDatoteke(posoba);

int main() {
	osoba head;
	head.next = NULL;
	bool run = true;
	IspisIzDatoteke(&head);
	printf("Dobro dosli u e-Banku!\n");
	while (run == true) {
		run = Banka(&head);
	}
	UpisUDatoteku(&head);
	return 0;
}

bool Banka(posoba head) {
	char od[10];
	int counter=0;
	posoba current;
	printf("Postojeci korisnik ili novi?\n-E -> Existing\n-N -> New\n-Izlaz\n"); scanf(" %s", od);
	while (strcmp(od,"N")==0 || strcmp(od,"n")==0) {
		system("cls");
		Registracija(head);
		printf("Postojeci korisnik ili novi?\n-E -> Existing\n-N -> New\n-Izlaz\n"); scanf(" %s", od);
	}
	if (strcmp(od, "izlaz") == 0 || strcmp(od,"Izlaz")==0) {
		return false;
	}
	if (head->next != NULL) {
		system("cls");
		printf("Prijavite se:\n");
		while ((current = Login(head)) == NULL) {
			counter++;
			if (counter == 5) {
				system("cls");
				printf("Oladite 30 sekundi!\n");
				return false;
			}
		}
	}
	else {
		system("cls");
		printf("Baza korisnika prazna...\n");
		return true;
	}
	
	return Korisnik(current,head);

}

unsigned int OIBprovjera() {
	unsigned int temp;
	unsigned int del;
	int counter = 0;
	while (1) {
		scanf(" %d", &temp);
		del = temp;
		while (del > 0) {
			del /= 10;
			counter++;
		}
		if (counter == 4) {
			return temp;
		}
		system("cls");
		printf("Oib je duljine 4 znamenki!\nUnesi ponovno: ");
		counter = 0;
	}
}

char* LozinkaProvjera() {
	char lozinka[15];
	int count1,count2,count3,count4;
	while (1) {
		scanf(" %s", lozinka);
		count1 = 0; count2 = 0; count3 = 0; count4 = 0;
		if (strlen(lozinka) < 8) {
			system("cls");
			printf("Lozinka mora biti duga najmanje 8 znakova, te sadrzavati veliko i malo slovo, broj i specijalni znak!\nUnesi ponovno: ");
			continue;
		}
		for (int i = 0; lozinka[i] != '\0'; i++) {
			if (lozinka[i] >= 33 && lozinka[i] <= 47) count1++;
			else if (lozinka[i] >= 48 && lozinka[i] <= 57) count2++;
			else if (lozinka[i] >= 65 && lozinka[i] <= 90) count3++;
			else if (lozinka[i] >= 97 && lozinka[i] <= 122) count4++;
		}
		if (count1 >= 1 && count2 >= 1 && count3 >= 1 && count4 >= 1) {
			return lozinka;
		}
		system("cls");
		printf("Lozinka mora biti duga najmanje 8 znakova, te sadrzavati veliko i malo slovo, broj i specijalni znak!\nUnesi ponovno: ");
	}
}

char* KImeProvjera(posoba head) {
	char kIme[15];
	if (head->next == NULL) {
		scanf(" %s", kIme);
		return kIme;
	}
	int flag = 0;
	posoba temp = head;
	while (1) {
		head = temp->next;
		scanf(" %s", kIme);
		while (head != NULL) {
			if (strcmp(kIme, head->korisnickiracun.korisnickoime) == 0) {
				system("cls");
				printf("Korisnicko ime vec postoji!\nUnesi ponovno: ");
				flag = 1;
			}
			head = head->next;
		}
		if (flag == 0) {
			return kIme;
		}
		flag = 0;
	}
}

int Registracija(posoba head) {
	posoba novi = NULL;
	novi = (posoba)malloc(sizeof(osoba));
	if (novi == NULL) {
		printf("Greska u alokaciji memorije...\n");
		return EXIT_FAILURE;
	}
	printf("Unesite vase ime: "); scanf(" %s", novi->ime);
	system("cls");
	printf("Unesite vase prezime: "); scanf(" %s", novi->prezime);
	system("cls");
	printf("Unesite vas oib: ");  novi->oib = OIBprovjera();
	system("cls");
	printf("Unesite vase korisnicko ime: "); strcpy(novi->korisnickiracun.korisnickoime, KImeProvjera(head));
	system("cls");
	printf("Unesite vasu lozinku: "); strcpy(novi->korisnickiracun.lozinka,LozinkaProvjera());
	system("cls");
	novi->korisnickiracun.head.next = NULL;
	novi->korisnickiracun.ustedevina = 0;
	novi->korisnickiracun.next = NULL;
	novi->next = head->next;
	head->next = novi;
	novi->korisnickiracun.head.red = 0;
	printf("Uspjesna registracija!\n");
	return EXIT_SUCCESS;
}

posoba Login(posoba head) {
	head = head->next;
	char ime[15];
	char lozinka[15];
	printf("Unesite korisnicko ime: "); scanf(" %s", ime);
	printf("Unesite lozinku: "); scanf(" %s", lozinka);
	while (head != NULL) {
		if (strcmp(ime, head->korisnickiracun.korisnickoime) == 0 && strcmp(lozinka, head->korisnickiracun.lozinka) == 0) {
			return head;
		}
		head = head->next;
	}
	system("cls");
	printf("Krivo ste unijeli korisnicko ime ili lozinku!\n");
	return NULL;
}

int Uplata(posoba current) {
	printf("Odaberite zeljenu kolicinu novca za uplatiti:\n");
	double iznos=0;
	while (1) {
		printf("5\t10\n20\t50\n100\t500\n0 - izlaz\n");
		scanf(" %lf", &iznos);
		if (iznos == 0) {
			system("cls");
			return EXIT_SUCCESS;
		}
		if (!(iznos != 5 && iznos != 10 && iznos != 20 && iznos != 50 && iznos != 100 && iznos != 500)) {
			current->korisnickiracun.ustedevina += iznos;
			UpisPovijest(current, "Uplata na racun", iznos);
			system("cls");
			return EXIT_SUCCESS;
		}
		system("cls");
		printf("Niste unijeli trazenu kolicinu, unesite opet:\n");
	}
}

int Isplata(posoba current) {
	printf("Odaberite zeljenu kolicinu novca za isplatiti:\n");
	double iznos = 0;
	while (1) {
		printf("5\t10\n20\t50\n100\t500\n0 - izlaz\n");
		scanf(" %lf", &iznos);
		if (iznos == 0) {
			system("cls");
			return EXIT_SUCCESS;
		}
		if (!(iznos != 5 && iznos != 10 && iznos != 20 && iznos != 50 && iznos != 100 && iznos != 500)) {
			current->korisnickiracun.ustedevina -= iznos;
			if (current->korisnickiracun.ustedevina >= 0) {
				UpisPovijest(current, "Isplata iz racuna", -iznos);
				system("cls");
				return EXIT_SUCCESS;
			}
			else {
				current->korisnickiracun.ustedevina += iznos;
				system("cls");
				printf("Nemozete isplatiti tu kolicinu, nemate dovoljno sredstava.\n");
				continue;
			}
		}
		system("cls");
		printf("Niste unijeli trazenu kolicinu, unesite opet:\n");
	}
}

int Placanje(posoba current, posoba head) {
	char opis[100];
	char trazi[15];
	char pronaden[15]="0";
	double kolicina;
	posoba temp = head->next;
	head = head->next;
	printf("Unesite korisnicko ime osobe kojoj zelite uplatiti ili exit za izlaz: ");
	while (strcmp(pronaden,"0")==0) {
		scanf(" %s", trazi);
		if (strcmp(trazi, "exit") == 0 || strcmp(trazi, "Exit") == 0) {
			system("cls");
			return EXIT_SUCCESS;
		}
		else if (strcmp(trazi, current->korisnickiracun.korisnickoime) != 0) {
			while (head != NULL) {
				if (strcmp(head->korisnickiracun.korisnickoime, trazi) == 0) {
					strcpy(pronaden, trazi);
					temp = head;
					break;
				}
				head = head->next;
			}
			if (head == NULL) {
				system("cls");
				printf("Korisnik nije pronaden. Pokusajte ponovno.\n");
			}
			head = temp;
		}
		else {
			system("cls");
			printf("Nemozete sami sebi poslati novac. Pokusajte ponovno.\n");
		}
	}
	printf("Unesite zeljenu kolicinu za uplatiti ili 0 za izlaz: ");
	while (1) {
		scanf(" %lf", &kolicina);
		if (kolicina > 0) {
			current->korisnickiracun.ustedevina -= kolicina;
			if (current->korisnickiracun.ustedevina < 0) {
				current->korisnickiracun.ustedevina += kolicina;
				system("cls");
				printf("Nemate dovoljno sredstava za prenijeti. Upisite novu kolicinu ili 0 za izlaz.\n");
				continue;
			}
			temp->korisnickiracun.ustedevina += kolicina;
			strcpy(opis, "Poslana sredstva korisniku ");
			strcat(opis, temp->korisnickiracun.korisnickoime);
			UpisPovijest(current, opis, -kolicina);
			strcpy(opis, "Primljena sredstva od korisnika ");
			strcat(opis, current->korisnickiracun.korisnickoime);
			UpisPovijest(temp, opis, kolicina);
			system("cls");
			return EXIT_SUCCESS;
		}
		else if (kolicina == 0) {
			system("cls");
			return EXIT_SUCCESS;
		}
		else {
			system("cls");
			printf("Neispravna kolicina unesena. Pokusajte ponovno.\n");
		}
	}
}

int UpisPovijest(posoba current,const char opis[], double iznos) {
	ptranzakcija novi = NULL;
	novi = (ptranzakcija)malloc(sizeof(tranzakcija));
	if (novi == NULL) {
		system("cls");
		printf("Greska u alokaciji memorije...\n");
		return EXIT_FAILURE;
	}
	current->korisnickiracun.head.red++;
	novi->red = current->korisnickiracun.head.red;
	strcpy(novi->vrsta, opis);
	novi->iznos = iznos;
	ptranzakcija temp = &current->korisnickiracun.head;
	novi->next = temp->next;
	temp->next = novi;
	return EXIT_SUCCESS;
}

int IspisPovijest(posoba current) {
	ptranzakcija head = &current->korisnickiracun.head;
	if (head->next == NULL) {
		system("cls");
		printf("Nema izvrsenih tranzakcija.\n");
		return EXIT_SUCCESS;
	}
	head = head->next;
	system("cls");
	while (head != NULL) {
		printf("%s: %lf\n", head->vrsta, head->iznos);
		head = head->next;
	}
	return EXIT_SUCCESS;
}

int Brisanje(posoba current, posoba head) {
	ptranzakcija temp = &current->korisnickiracun.head;
	ptranzakcija del;
	if (temp->next != NULL) {
		del = temp->next;
		while (temp != NULL) {
			temp = del->next;
			free(del);
			del = temp;
		}
	}
	while (head->next != current) {
		head = head->next;
	}
	head->next = current->next;
	free(current);
	return EXIT_SUCCESS;
}

bool Korisnik(posoba current, posoba head) {
	char odabir[15];
	bool ret;
	system("cls");
	while (1) {
		printf("Koju radnju zelite obaviti?\n-Stanje\n-Uplata\n-Isplata\n-Placanje\n-Povijest\n-Odjava\n-Mijenjanje podataka\n-Brisanje racuna\n-Izlaz\n"); scanf(" %s", odabir);
		if (strcmp(odabir, "stanje") == 0 || strcmp(odabir, "Stanje") == 0) {
			system("cls");
			printf("Trenutno stanje na racunu je: %lf\n", current->korisnickiracun.ustedevina);
		}
		else if (strcmp(odabir, "uplata") == 0 || strcmp(odabir, "Uplata") == 0) {
			system("cls");
			Uplata(current);
		}
		else if (strcmp(odabir, "isplata") == 0 || strcmp(odabir, "Isplata") == 0) {
			system("cls");
			Isplata(current);
		}
		else if (strcmp(odabir, "placanje") == 0 || strcmp(odabir, "Placanje") == 0) {
			system("cls");
			Placanje(current, head);
		}
		else if (strcmp(odabir, "povijest") == 0 || strcmp(odabir, "Povijest") == 0) {
			system("cls");
			IspisPovijest(current);
		}
		else if (strcmp(odabir, "odjava") == 0 || strcmp(odabir, "Odjava") == 0) {
			system("cls");
			ret = true;
			break;
		}
		else if (strcmp(odabir, "mijenjanje") == 0 || strcmp(odabir, "Mijenjanje") == 0) {
			system("cls");
			while (1) {
				printf("Podatak za izmjenu:\n-Ime\n-Prezime\n-OIB\n-Korisnicko ime\n-Lozinka\n-Izlaz\n"); scanf(" %s", odabir);
				if (strcmp(odabir, "ime") == 0 || strcmp(odabir, "Ime") == 0) {
					system("cls");
					printf("Unesite novo ime: "); scanf(" %s", odabir);
					strcpy(current->ime, odabir);
					system("cls");
				}
				else if (strcmp(odabir, "prezime") == 0 || strcmp(odabir, "Prezime") == 0) {
					system("cls");
					printf("Unesite novo prezime: "); scanf(" %s", odabir);
					strcpy(current->prezime, odabir);
					system("cls");
				}
				else if (strcmp(odabir, "oib") == 0 || strcmp(odabir, "Oib") == 0) {
					system("cls");
					printf("Unesite novi oib: ");
					current->oib = OIBprovjera();
					system("cls");
				}
				else if (strcmp(odabir, "korisnicko") == 0 || strcmp(odabir, "Korisnicko") == 0) {
					system("cls");
					printf("Unesite novo korisnicko ime: ");
					strcpy(current->korisnickiracun.korisnickoime, KImeProvjera(head));
					system("cls");
				}
				else if (strcmp(odabir, "lozinka") == 0 || strcmp(odabir, "Lozinka") == 0) {
					system("cls");
					printf("Unesite staru lozinku: "); scanf(" %s", odabir);
					if (strcmp(odabir, current->korisnickiracun.lozinka) == 0) {
						system("cls");
						printf("Unesite novu lozinku: ");
						strcpy(current->korisnickiracun.lozinka, LozinkaProvjera());
						system("cls");
					}
					else {
						system("cls");
						printf("Unesena netocna stara lozinka.\n");
					}
				}
				else if (strcmp(odabir, "izlaz") == 0 || strcmp(odabir, "Izlaz") == 0) {
					system("cls");
					break;
				}
				else {
					system("cls");
					printf("Nepoznata naredba unesena. Pokusajte ponovno.");
				}
			}
		}
		else if (strcmp(odabir, "Brisanje") == 0 || strcmp(odabir, "brisanje") == 0) {
			system("cls");
			printf("Je li stvarno zelite obrisati racun? Da/Ne "); scanf(" %s", odabir);
			if (strcmp(odabir, "Da") == 0 || strcmp(odabir, "da") == 0) {
				Brisanje(current, head);
				system("cls");
				ret = true;
				break;
			}
			system("cls");
		}
		else if (strcmp(odabir, "izlaz") == 0 || strcmp(odabir, "Izlaz") == 0) {
			system("cls");
			ret = false;
			break;
		}
		else {
			system("cls");
			printf("Unesena nepoznata naredba, pokusajte ponovno.\n");
		}
	}
	return ret;
}

int UpisUDatoteku(posoba head) {
	FILE* dat = NULL;
	dat = fopen("podatci.txt", "w");
	if (!dat) {
		printf("Pogreska u upisivanju datoteke...\n");
		return EXIT_FAILURE;
	}
	if (head->next == NULL) {
		return EXIT_FAILURE;
	}
	head = head->next;
	ptranzakcija phead;
	while (head != NULL) {
		fprintf(dat, "%s %s %d\n%s %s %lf\n", head->ime, head->prezime, head->oib, head->korisnickiracun.korisnickoime, head->korisnickiracun.lozinka, head->korisnickiracun.ustedevina);
		fprintf(dat, "%d\n", head->korisnickiracun.head.red);
		phead = head->korisnickiracun.head.next;
		if (phead != NULL) {
			while (phead != NULL) {
				fprintf(dat, "%s\t%lf\t%d\n", phead->vrsta, phead->iznos,phead->red);
				phead = phead->next;
			}
		}
		fprintf(dat,"\n");
		head = head->next;
	}
	fclose(dat);
	return EXIT_SUCCESS;
}

int IspisIzDatoteke(posoba head) {
	FILE* dat = NULL;
	dat = fopen("podatci.txt", "r");
	if (!dat) {
		printf("Pogreska u citanju datoteke...\n");
		return EXIT_FAILURE;
	}
	char a;
	int i;
	posoba novi=NULL;
	ptranzakcija tranz = NULL;
	ptranzakcija temp;
	while (1) {
		novi = (posoba)malloc(sizeof(osoba));
		if (novi == NULL) {
			printf("Greska u alociranju memorije...\n");
			return EXIT_FAILURE;
		}
		if (fscanf(dat, "%s %s %d", novi->ime, novi->prezime, &novi->oib) < 3) {
			free(novi);
			break;
		}
		fgetc(dat);
		fscanf(dat, "%s %s %lf", novi->korisnickiracun.korisnickoime, novi->korisnickiracun.lozinka, &novi->korisnickiracun.ustedevina); fgetc(dat);
		fscanf(dat, "%d", &novi->korisnickiracun.head.red); fgetc(dat);
		novi->korisnickiracun.head.next = NULL;
		a = fgetc(dat);
		if (a != '\n') {
			while (a != '\n') {
				tranz = (ptranzakcija)malloc(sizeof(tranzakcija));
				if (tranz == NULL) {
					printf("Greska u alociranju memorije...\n");
					return EXIT_FAILURE;
				}
				for (i = 0; a != '\t'; i++) {
					tranz->vrsta[i] = a;
					a = fgetc(dat);
				}
				tranz->vrsta[i] = '\0';
				fscanf(dat, "%lf", &tranz->iznos); fgetc(dat);
				fscanf(dat, "%d", &tranz->red); fgetc(dat);
				a = fgetc(dat);
				temp = &novi->korisnickiracun.head;
				if (temp->next != NULL) {
					temp = temp->next;
					while (temp->next != NULL) {
						if (temp->red > tranz->red) {
							temp = temp->next;
						}
					}
					tranz->next = temp->next;
					temp->next = tranz;
				}
				else {
					tranz->next = temp->next;
					temp->next = tranz;
				}
				tranz = NULL;
			}
		}
		novi->next = head->next;
		head->next = novi;
		novi = NULL;
	}
	return 0;
}