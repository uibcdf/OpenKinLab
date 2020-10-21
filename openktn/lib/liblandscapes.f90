MODULE MODULE_LANDSCAPES

USE MODULE_SORT

CONTAINS

!SUBROUTINE BOTTOM_UP_1D(x, y, T_start, T_ind, T_pn, n_nodes, n_edges)
!
!    IMPLICIT NONE
!
!    TYPE array_pointer
!        INTEGER,DIMENSION(:),POINTER::p1
!    END TYPE array_pointer
!
!
!    INTEGER,INTENT(IN)::n_nodes,n_edges
!    INTEGER,DIMENSION(n_edges),INTENT(IN)::T_ind
!    INTEGER,DIMENSION(n_nodes+1),INTENT(IN)::T_start
!    DOUBLE PRECISION, DIMENSION(n_nodes),INTENT(IN)::T_pn
!    DOUBLE PRECISION, DIMENSION(n_nodes),INTENT(OUT)::x,y
!
!    INTEGER, DIMENSION(n_nodes):: order, belongs_to
!    LOGICAL, DIMENSION(n_nodes):: checked
!
!    TYPE(array_pointer),DIMENSION(:),POINTER::basin
!    INTEGER, DIMENSION(:), ALLOCATABLE:: basin_lmin, basin_lmax, basin_coin
!    INTEGER::n_basins
!
!    INTEGER, DIMENSION
!
!    CALL ARGSORT_REVERSE(T_pn, order) 
!
!    x(:)=0.0d0
!    y(:)=T_pn(:)
!
!    checked(:)=.FALSE.
!    belongs_to=0
!    n_basins=0
!
!    ALLOCATE(basin_lmin(n_basins), basin_lmax(n_basins), basin_coin(n_basins))
!    ALLOCATE()
!
!    DO ii=1, n_nodes
!
!        ind_node = order(ii)
!
!        new_basin = .True.
!
!        DO jj=T_start(ind_node)+1, T_start(ind_node+1)
!            
!            IF (checked(jj).eqv..True.) THEN
!
!                new_basin = .False.
!
!            END IF
!
!        END DO
!
!        IF (new_basin.eqv..True.) THEN
!
!            n_basins = n_basins+1
!            belongs_to(ind_node)=n_basins
!
!            
!    
!
!END SUBROUTINE BOTTOM_UP_1D


END MODULE MODULE_LANDSCAPES

!! f2py --f90flags='-fast' -c -m pyn_fort_net pyn_fort_net.f90
!!f2py --f90flags='-fast' -c -m pyn_fort_net pyn_fort_net.f90 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lmkl_def -lpthread

