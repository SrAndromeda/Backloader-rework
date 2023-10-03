import Loadable from 'app/components/Loadable';
import { lazy } from 'react';

const AppOutletList = Loadable(lazy(() => import('./list/AppOutletList')));


const outletRoutes = [
    {
        path: '/outlets',
        element: <AppOutletList />
    }
];

export default outletRoutes;