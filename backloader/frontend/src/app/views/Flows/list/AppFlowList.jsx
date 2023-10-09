import { Box, Button, Fab, Icon, IconButton, styled } from "@mui/material";
import { Breadcrumb, SimpleCard } from "app/components";
import ObjectsTable from "app/components/ObjectsTable";
import { Span } from "app/components/Typography";
import axios from "axios";
import { BASE_BACKEND, BASE_FLOW, BASE_OUTLET } from "app/utils/constant";
import ResponsiveDialog from "app/components/ResponsiveDialog";
import SimpleDialog from "app/components/SimpleDialog";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ViewModal from "./ViewModal";
import { fetchFlow, fetchOutlet } from 'app/utils/fetchData'

const Container = styled("div")(({ theme }) => ({
  margin: "30px",
  [theme.breakpoints.down("sm")]: { margin: "16px" },
  "& .breadcrumb": {
    marginBottom: "30px",
    [theme.breakpoints.down("sm")]: { marginBottom: "16px" },
  },
}));

const StyledButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(1),
}));

function deleteFlow(id, setTitle, setContent, setOpen){
  axios.delete(BASE_BACKEND + BASE_FLOW, {data:{
    id: id
  }})
    .then((response) => {
      setTitle('Flow deleted succesfully')
      setOpen(true)
    })
    .catch((error) => {
      setTitle('Error deleting flow')
      setContent(error.message)
      setOpen(true)
    })
}

function getOutletByID(id, array){
  for (let i = 0; i < array.length; i++) {
    const element = array[i];
    if(element.id == id){
      return element;
    }
  }
}

const AppFlowList = () => {

  const [refresh, setRefresh] = useState(0);
  const keyContent = ['id', 'name', 'url'];
  const headers = ['#', 'Name', 'URL'];
  const [content, setContent] = useState([]);
  const [outletContent, setOutletContent] = useState([]);
  const navigation = useNavigate();
  const [openDelete, setOpenDelete] = useState(false);
  const [openAlert, setOpenAlert] = useState(false);
  const [titleAlert, setTitleAlert] = useState('');
  const [contentAlert, setContentAlert] = useState('');
  const [active, setActive] = useState(-1);
  const [openView, setOpenView] = useState(false);

  const getFlowActive = () => {
    if(active != -1){
      return {
        ...content[active],
        'outlet': getOutletByID(content[active].outlet_id, outletContent)
      }
    }
    return null
  }

  useEffect (() => {
      fetchFlow(setContent)
      fetchOutlet(setOutletContent)
      setActive(-1)
  },[refresh])

  return (
    <Container>
      <Box className="breadcrumb">
        <Breadcrumb routeSegments={[{ name: "Flows", path: "/flows" }]} />
      </Box>

      <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'flex-end'}}>
        <StyledButton variant="contained" color="success" onClick={()=>{navigation('/flows/create')}}>
          <Icon sx={{ mr: 2 }}>add</Icon>
          <Span>New</Span>
        </StyledButton>
      </div>

      <SimpleCard>
        <ObjectsTable
          headers={headers}
          keyContent={keyContent}
          content={content}
          pagination={false}
          viewButton={true}
          viewAction={(index)=>{setActive(index); setOpenView(true)}}
          editButton={false}
          editAction={(index)=>{navigation('/flow/edit/'+content[index].id)}}
          deleteButton={true}
          deleteAction={(index)=>{setActive(index); setOpenDelete(true)}}
        />
      </SimpleCard>
      <ResponsiveDialog
        open={openDelete}
        setOpen={setOpenDelete}
        title={active == -1 ? ('') : ('Delete flow ' + content[active].name + '?')}
        contentText={'Are you sure you want to delete this flow? This will break associated flows'}
        acceptAction={()=>{deleteFlow(content[active].id, setTitleAlert, setContentAlert, setOpenAlert); setOpenDelete(false)}}
      />
      <SimpleDialog 
        open={openAlert}
        setOpen={setOpenAlert}
        title={titleAlert}
        contentText={contentAlert}
        handleClose={()=>{setOpenAlert(false);setRefresh(refresh+1)}}
      />
      <ViewModal 
        open={openView}
        setOpen={setOpenView}
        flow={getFlowActive()}
      />
    </Container>
  );
};

export default AppFlowList;