#ifndef HASHTAB_H
#define HASHTAB_H


struct cvorListe;
typedef struct cvorListe* Pozicija;
typedef struct cvorListe** Lista;
typedef struct cvorListe {
	int HIme;
	int HLozinka;
	Pozicija next;
}Cvor;

struct Hash;
typedef struct Hash* PozicijaHash;
typedef struct Hash {
	int velicina;
	Lista NizCvorova;
}HashT;

int InitTablice(PozicijaHash,int);
int Hash(const char[]);
int SljedeciPrBr(int);
int DodajUHashTab(const char [], const char [], PozicijaHash);
int BrisiUHashTab(const char[], const char[], PozicijaHash);
bool JeLiUHashTab(const char[], const char[], PozicijaHash);
int IzbrisiSveUHashTab(PozicijaHash);

#endif