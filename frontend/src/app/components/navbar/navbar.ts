import { Component, inject } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  authService = inject(AuthService);
  router = inject(Router);

  // Use Observable directly for AsyncPipe in HTML if desired, or subscribe
  currentUser$ = this.authService.currentUser$;

  logout() {
    this.authService.logout();
  }
}
