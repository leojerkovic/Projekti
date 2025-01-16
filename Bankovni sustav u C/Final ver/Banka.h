#ifndef BANKA_H
#define BANKA_H

#include "Hashtab.h"

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
bool Banka(posoba, PozicijaHash);
int Registracija(posoba, PozicijaHash);
posoba Login(posoba, PozicijaHash);
bool Korisnik(posoba, posoba, PozicijaHash);
bool Admin(posoba, PozicijaHash);
int Uplata(posoba);
int Isplata(posoba);
int Placanje(posoba, posoba);
int UpisPovijest(posoba, const char[], double);
int IspisPovijest(posoba);
int Brisanje(posoba, posoba, const char[], PozicijaHash);
int BrisanjeSve(posoba);
int Izlistati(posoba);
int UpisUDatoteku(posoba);
int IspisIzDatoteke(posoba);
int IspisIzDatotekeHash(PozicijaHash);
int UpisUDatotekuHash(PozicijaHash);

#endif