import { Injectable, inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map } from 'rxjs';

export const adminGuard: CanActivateFn = (route, state) => {
    const authService = inject(AuthService);
    const router = inject(Router);

    return authService.currentUser$.pipe(
        map(user => {
            // Assuming Role 3 is Administrator
            if (user && user.idTipoUsuario === 3) {
                return true;
            }
            return router.createUrlTree(['/login']);
        })
    );
};
