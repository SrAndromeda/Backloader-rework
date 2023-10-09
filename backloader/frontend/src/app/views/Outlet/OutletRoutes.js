import Loadable from 'app/components/Loadable';
import { lazy } from 'react';

const AppOutletList = Loadable(lazy(() => import('./list/AppOutletList')));
const AppOutletCreate = Loadable(lazy(() => import('./create/AppOutletCreate')));


const outletRoutes = [
    {
        path: '/outlets',
        element: <AppOutletList />
    },
    {
        path: '/outlets/create',
        element: <AppOutletCreate />
    }
];

export default outletRoutes;