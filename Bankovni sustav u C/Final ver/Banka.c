#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "Banka.h"
#include "Hashtab.h"

int main() {
	osoba head;
	head.next = NULL;
	HashT Sensitive;
	InitTablice(&Sensitive,25);
	bool run = true;
	IspisIzDatoteke(&head);
	IspisIzDatotekeHash(&Sensitive);
	printf("Dobro dosli u e-Banku!\n");
	while (run == true) {
		run = Banka(&head,&Sensitive);
	}
	UpisUDatoteku(&head);
	UpisUDatotekuHash(&Sensitive);
	return 0;
}

bool Banka(posoba head,PozicijaHash Tab) {
	char od[10];
	int counter=0;
	posoba current;
	printf("Postojeci korisnik ili novi?\n-E -> Existing\n-N -> New\n-Izlaz\n"); scanf(" %s", od);
	while (strcmp(od,"N")==0 || strcmp(od,"n")==0) {
		system("cls");
		Registracija(head,Tab);
		printf("Postojeci korisnik ili novi?\n-E -> Existing\n-N -> New\n-Izlaz\n"); scanf(" %s", od);
	}
	if (strcmp(od, "izlaz") == 0 || strcmp(od,"Izlaz")==0) {
		return false;
	}
	if (strcmp(od, "ADMIN") == 0) {
		return Admin(head,Tab);
	}
	if (strcmp(od, "E") == 0 || strcmp(od, "e") == 0) {
		if (head->next == NULL) {
			system("cls");
			printf("Baza korisnika prazna...\n");
			return true;
		}
		system("cls");
		printf("Prijavite se:\n");
		while ((current = Login(head,Tab)) == NULL) {
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
		printf("Unesena nepoznata naredba...\n");
		return true;
	}
	return Korisnik(current,head,Tab);

}

bool Admin(posoba head, PozicijaHash Tab) {
	char odabir[15];
	bool ret;
	system("cls");
	while (1) {
		printf("ADMIN - Koju radnju zelite obaviti?\n-Izlistat korisnike\n-Obrisi sve\n-Odjava\n-Izlaz\n"); scanf(" %s", odabir);
		if (strcmp(odabir, "izlistat") == 0 || strcmp(odabir, "Izlistat") == 0) {
			system("cls");
			Izlistati(head);
		}
		else if (strcmp(odabir, "obrisi") == 0 || strcmp(odabir, "Obrisi") == 0) {
			system("cls");
			printf("Unesite POTVRDA za kompletno brisanje, ostali unosi vracaju na pocetak: "); scanf(" %s", odabir);
			if (strcmp("POTVRDA", odabir) == 0) {
				system("cls");
				IzbrisiSveUHashTab(Tab);
				BrisanjeSve(head);
				printf("Uspjesno baza obrisana.\n");
			}
			else {
				system("cls");
			}
		}
		else if (strcmp(odabir, "odjava") == 0 || strcmp(odabir, "Odjava") == 0) {
			system("cls");
			ret = true;
			break;
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

int Izlistati(posoba head) {
	if (head->next == NULL) {
		printf("Nema korisnika u bazi...\n");
		return EXIT_FAILURE;
	}
	head = head->next;
	while (head != NULL) {
		printf("Ime korisnika: %s %s\n", head->ime, head->prezime);
		printf("OIB: %d\n", head->oib);
		printf("Korisnicko ime: %s\n", head->korisnickiracun.korisnickoime);
		printf("Iznos na racunu: %lf\n", head->korisnickiracun.ustedevina);
		printf("Povijest tranzakcija (prema vrhu novije):\n");
		IspisPovijest(head);
		printf("\n");
		head = head->next;
	}
	return EXIT_SUCCESS;
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

int Registracija(posoba head,PozicijaHash Tab) {
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
	printf("Unesite vasu lozinku: "); DodajUHashTab(novi->korisnickiracun.korisnickoime, LozinkaProvjera(), Tab);
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

posoba Login(posoba head,PozicijaHash Tab) {
	head = head->next;
	char ime[15];
	char lozinka[15];
	printf("Unesite korisnicko ime: "); scanf(" %s", ime);
	printf("Unesite lozinku: "); scanf(" %s", lozinka);
	while (head != NULL) {
		if (JeLiUHashTab(ime,lozinka,Tab) && strcmp(head->korisnickiracun.korisnickoime,ime)==0) {
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
		printf("Nema izvrsenih tranzakcija.\n");
		return EXIT_SUCCESS;
	}
	head = head->next;
	while (head != NULL) {
		printf("%s: %lf\n", head->vrsta, head->iznos);
		head = head->next;
	}
	return EXIT_SUCCESS;
}

int Brisanje(posoba current, posoba head, const char loz[], PozicijaHash Tab) {
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
	BrisiUHashTab(current->korisnickiracun.korisnickoime, loz, Tab);
	free(current);
	return EXIT_SUCCESS;
}

int BrisanjeSve(posoba head) {
	if (head->next == NULL) {
		printf("Nema korisnika za brisanje...\n");
		return EXIT_FAILURE;
	}
	posoba current;
	ptranzakcija temp;
	ptranzakcija del;
	while (head->next != NULL) {
		current = head->next;
		temp = &current->korisnickiracun.head;
		if (temp->next != NULL) {
			del = temp->next;
			while (temp != NULL) {
				temp = del->next;
				free(del);
				del = temp;
			}
		}
		head->next = current->next;
		free(current);
	}
	return EXIT_SUCCESS;
}

bool Korisnik(posoba current, posoba head, PozicijaHash Tab) {
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
					printf("Unesite lozinku: "); scanf(" %s", odabir);
					if (JeLiUHashTab(current->korisnickiracun.korisnickoime, odabir, Tab)) {
						system("cls");
						printf("Unesite novo korisnicko ime: ");
						BrisiUHashTab(current->korisnickiracun.korisnickoime, odabir, Tab);
						strcpy(current->korisnickiracun.korisnickoime, KImeProvjera(head));
						DodajUHashTab(current->korisnickiracun.korisnickoime, odabir, Tab);
						system("cls");
					}
					else {
						system("cls");
						printf("Unesena netocna lozinka.\n");
					}
				}
				else if (strcmp(odabir, "lozinka") == 0 || strcmp(odabir, "Lozinka") == 0) {
					system("cls");
					printf("Unesite staru lozinku: "); scanf(" %s", odabir);
					if (JeLiUHashTab(current->korisnickiracun.korisnickoime,odabir,Tab)) {
						system("cls");
						printf("Unesite novu lozinku: ");
						BrisiUHashTab(current->korisnickiracun.korisnickoime, odabir, Tab);
						DodajUHashTab(current->korisnickiracun.korisnickoime, LozinkaProvjera(),Tab);
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
			printf("Unesite trenutnu lozinku za brisanje racuna: "); scanf(" %s", odabir);
			if (JeLiUHashTab(current->korisnickiracun.korisnickoime,odabir,Tab)) {
				Brisanje(current, head,odabir,Tab);
				system("cls");
				printf("Racun je uspjesno izbrisan!\n");
				ret = true;
				break;
			}
			system("cls");
			printf("Upisana netocna lozinka!\n");
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
		fprintf(dat, "%s %s %d\n%s %lf\n", head->ime, head->prezime, head->oib, head->korisnickiracun.korisnickoime, head->korisnickiracun.ustedevina);
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
		fscanf(dat, "%s %lf", novi->korisnickiracun.korisnickoime, &novi->korisnickiracun.ustedevina); fgetc(dat);
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
	fclose(dat);
	return EXIT_SUCCESS;
}

int UpisUDatotekuHash(PozicijaHash Tab) {
	FILE* dat = NULL;
	dat = fopen("podatcihash.txt", "w");
	if (!dat) {
		printf("Pogreska u upisivanju datoteke...\n");
		return EXIT_FAILURE;
	}
	Pozicija temp;
	int n = 0;
	fprintf(dat, "%d\n", Tab->velicina);
	for (int i = 0; i < Tab->velicina; i++) {
		if (Tab->NizCvorova[i] != NULL) {
			n++;
		}
	}
	fprintf(dat, "%d\n", n);
	for (int i = 0; i < Tab->velicina; i++) {
		int j = 0;
		if (Tab->NizCvorova[i] != NULL) {
			temp = Tab->NizCvorova[i];
			while (temp != NULL) {
				j++;
				temp = temp->next;
			}
			temp = Tab->NizCvorova[i];
			fprintf(dat, "%d %d\n", i, j);
			j = 0;
			while (temp != NULL) {
				fprintf(dat, "%d %d\n", temp->HIme, temp->HLozinka);
				temp = temp->next;
			}
		}
	}
	fclose(dat);
	return EXIT_SUCCESS;
}

int IspisIzDatotekeHash(PozicijaHash Tab) {
	FILE* dat = NULL;
	dat = fopen("podatcihash.txt", "r");
	if (!dat) {
		printf("Pogreska u citanju datoteke...\n");
		return EXIT_FAILURE;
	}
	int n;
	Pozicija zam=NULL;
	int poz, num;
	if (fscanf(dat, "%d\n", &Tab->velicina) < 1) {
		printf("Datoteka je prazna...\n");
		return EXIT_FAILURE;
	};
	fscanf(dat, "%d\n", &n);
	for (int i = 0; i < n; i++) {
		fscanf(dat, "%d %d\n", &poz, &num);
		for (int j = 0; j < num; j++) {
			zam = (Pozicija)malloc(sizeof(Cvor));
			if (zam == NULL) {
				printf("Greska u alokaciji memorije...");
				return EXIT_FAILURE;
			}
			fscanf(dat, "%d %d\n", &zam->HIme, &zam->HLozinka);
			zam->next = Tab->NizCvorova[zam->HLozinka % Tab->velicina];
			Tab->NizCvorova[zam->HLozinka % Tab->velicina] = zam;
			zam = NULL;
		}
	}
	fclose(dat);
	return EXIT_SUCCESS;
}