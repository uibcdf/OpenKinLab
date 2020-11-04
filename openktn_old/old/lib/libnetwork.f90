MODULE MODULE_NETWORK

USE MODULE_SORT

CONTAINS

SUBROUTINE SORTED_NODES_BY_PROBABILITY(order, T_pn, n_nodes)

    IMPLICIT NONE

    INTEGER, INTENT(IN):: n_nodes
    DOUBLE PRECISION, DIMENSION(n_nodes), INTENT(IN):: T_pn
    INTEGER, DIMENSION(n_nodes), INTENT(OUT):: order

    CALL ARGSORT_REVERSE(T_pn, order)

    order(:)=order(:)-1

END SUBROUTINE

SUBROUTINE COMPONENTS(num_comp,componente,T_start,T_ind,n_nodes,n_edges)

    IMPLICIT NONE
    
    INTEGER,INTENT(IN)::n_nodes,n_edges
    INTEGER,DIMENSION(n_edges),INTENT(IN)::T_ind
    INTEGER,DIMENSION(n_nodes+1),INTENT(IN)::T_start
    
    
    INTEGER,DIMENSION(n_nodes),INTENT(OUT)::componente
    INTEGER,INTENT(OUT)::num_comp
    
    INTEGER::i,j,jj,g,gg,h
    
    componente=0
    num_comp=0
    
    DO i=1,n_nodes
       
        IF (componente(i)==0) THEN
            num_comp=num_comp+1
            g=num_comp
            componente(i)=g
        ELSE
            g=componente(i)
        END IF
        
        DO j=T_start(i)+1,T_start(i+1)
            jj=T_ind(j)
            IF (componente(jj)==0) THEN
                componente(jj)=g
            ELSE
                IF (componente(jj)/=g) THEN
                    IF (componente(jj)<g) THEN
                        gg=componente(jj)
                    ELSE
                        gg=g
                        g=componente(jj)
                    END IF
                    DO h=1,n_nodes
                        IF (componente(h)==g) THEN
                            componente(h)=gg
                        ELSE
                            IF (componente(h)>g) componente(h)=componente(h)-1
                        END IF
                    END DO
                    g=gg
                    num_comp=num_comp-1
                END IF
            END IF
        END DO
    END DO

    componente=componente-1

END SUBROUTINE COMPONENTS


END MODULE MODULE_NETWORK

!! f2py --f90flags='-fast' -c -m pyn_fort_net pyn_fort_net.f90
!!f2py --f90flags='-fast' -c -m pyn_fort_net pyn_fort_net.f90 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lmkl_def -lpthread

