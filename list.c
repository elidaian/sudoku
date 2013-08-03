#include "list.h"
#ifndef NULL
#define NULL 0
#endif
INLINE t_lnode *ListGetFirst(t_list *ls)
{
	return ls->first;
}

INLINE t_lnode *ListGetLast(t_list *ls)
{
	return ls->last;
}

INLINE int ListGetNum(t_list *ls)
{
	return ls->num;
}

INLINE t_lnode *ListGetNext(t_lnode *n)
{
	return n->next;
}

INLINE t_lnode *ListGetPrev(t_lnode *n)
{
	return n->prev;
}

INLINE void ListReset(t_list *ls)
{
	ls->first=NULL;
	ls->last=NULL;
	ls->num=0;
}
INLINE void ListInsert(t_list *ls, t_lnode *n)
{
	n->prev=NULL;
	if((n->next=ls->first))
		n->next->prev=n;
	else
		ls->last=n;
	ls->first=n;
	ls->num++;
}
INLINE void ListAppend(t_list *ls,t_lnode *n)
{
	n->next=NULL;
	if((n->prev=ls->last))
		n->prev->next=n;
	else
		ls->first=n;
	ls->last=n;
	ls->num++;
}
INLINE void ListExtract(t_list *ls,t_lnode *n)
{
	if(n->next)
		n->next->prev=n->prev;
	else
		ls->last=n->prev;
	if(n->prev)
		n->prev->next=n->next;
	else
		ls->first=n->next;
	ls->num--;
}
