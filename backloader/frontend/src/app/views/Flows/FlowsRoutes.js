import Loadable from 'app/components/Loadable';
import { lazy } from 'react';

const AppFlowList = Loadable(lazy(() => import('./list/AppFlowList')));
const AppFlowCreate = Loadable(lazy(() => import('./create/AppFlowCreate')));

const flowsRoutes = [
    {
        path: '/flows',
        element: <AppFlowList />
    },
    {
        path: '/flows/create',
        element: <AppFlowCreate />
    }
];

export default flowsRoutes;