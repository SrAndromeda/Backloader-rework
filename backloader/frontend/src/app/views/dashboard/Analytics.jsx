import { Card, Grid, styled, useTheme } from '@mui/material';
import { Fragment, useEffect, useState } from 'react';
import { fetchFlow, fetchOutlet } from 'app/utils/fetchData'
import { SimpleCard } from 'app/components';
import ObjectsTable from 'app/components/ObjectsTable';

const ContentBox = styled('div')(({ theme }) => ({
  margin: '30px',
  [theme.breakpoints.down('sm')]: { margin: '16px' },
}));

const Title = styled('span')(() => ({
  fontSize: '1rem',
  fontWeight: '500',
  marginRight: '.5rem',
  textTransform: 'capitalize',
}));

const SubTitle = styled('span')(({ theme }) => ({
  fontSize: '0.875rem',
  color: theme.palette.text.secondary,
}));

const H4 = styled('h4')(({ theme }) => ({
  fontSize: '1rem',
  fontWeight: '500',
  marginBottom: '16px',
  textTransform: 'capitalize',
  color: theme.palette.text.secondary,
}));

const Analytics = () => {
  const { palette } = useTheme();
  const flowHeaders = ['#', 'Name', 'URL'];
  const flowKeyContent = ['id', 'name', 'url'];
  const [flowContent, setFlowContent] = useState([])
  const outletHeaders = ['#', 'Name', 'Path'];
  const outletKeyContent = ['id', 'name', 'path'];
  const [outletContent, setOutletContent] = useState([])

  useEffect(() => {
    fetchFlow(setFlowContent)
    fetchOutlet(setOutletContent)
  }, [])

  return (
    <Fragment>
      <ContentBox className="analytics">
        {/* <Grid container spacing={3}>
          <Grid item lg={8} md={8} sm={12} xs={12}> */}
            <SimpleCard title={'Flows'}>
              <ObjectsTable
                headers={flowHeaders}
                keyContent={flowKeyContent}
                content={flowContent}
                pagination={true}
              />
            </SimpleCard>
            <SimpleCard title={'Outlets'}>
              <ObjectsTable
                headers={outletHeaders}
                keyContent={outletKeyContent}
                content={outletContent}
                pagination={true}
              />
            </SimpleCard>
          {/* </Grid>
        </Grid> */}
      </ContentBox>
    </Fragment>
  );
};

export default Analytics;
