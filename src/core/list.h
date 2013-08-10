#ifndef _LINKED_LIST_H_
#define _LINKED_LIST_H_
typedef struct s_lnode
{
	struct s_lnode *next;
	struct s_lnode *prev;
}
t_lnode;
typedef struct s_list
{
	t_lnode *first;
	t_lnode *last;
	int num;
}
t_list;
#define GET_ELEM(TYPE,NODE,FIELD)((TYPE*)((long)(NODE)-(long)&((TYPE*)0)->FIELD))
#ifdef INLINE
#undef INLINE
#endif
#define INLINE
INLINE t_lnode *ListGetFirst(t_list *ls);
INLINE t_lnode *ListGetLast(t_list *ls);
INLINE int ListGetNum(t_list *ls);
INLINE t_lnode *ListGetNext(t_lnode *n);
INLINE t_lnode *ListGetPrev(t_lnode *n);
INLINE void ListReset(t_list *ls);
INLINE void ListInsert(t_list *ls,t_lnode *n);
INLINE void ListAppend(t_list *ls,t_lnode *n);
INLINE void ListExtract(t_list *ls,t_lnode *n);
#endif
