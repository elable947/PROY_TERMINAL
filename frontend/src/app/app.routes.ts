import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { LoginComponent } from './components/login/login.component';
import { Register } from './components/register/register';
import { adminGuard } from './guards/admin.guard';
import { authGuard } from './guards/auth.guard';
import { AdminDashboardComponent } from './components/admin-dashboard/admin-dashboard.component';

import { ProfileComponent } from './components/profile/profile.component';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: Register },
    { path: 'admin', component: AdminDashboardComponent, canActivate: [authGuard, adminGuard] }, // Modified admin route
    { path: 'profile', component: ProfileComponent, canActivate: [authGuard] }, // Modified profile route
    { path: 'my-trips', loadComponent: () => import('./components/my-trips/my-trips.component').then(m => m.MyTripsComponent), canActivate: [authGuard] }, // Added my-trips route
    { path: 'company', loadComponent: () => import('./components/company-dashboard/company-dashboard').then(m => m.CompanyDashboard) },
    { path: 'driver', loadComponent: () => import('./components/driver-dashboard/driver-dashboard.component').then(m => m.DriverDashboardComponent) },
    { path: 'public-companies', loadComponent: () => import('./components/public-companies/public-companies.component').then(m => m.PublicCompaniesComponent) },
    { path: 'trips', loadComponent: () => import('./components/public-trips/public-trips.component').then(m => m.PublicTripsComponent) },
    { path: '**', redirectTo: '' }
];
