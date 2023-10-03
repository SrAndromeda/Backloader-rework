import { Box, Button, Fab, Icon, IconButton, styled } from "@mui/material";
import { Breadcrumb, SimpleCard } from "app/components";
import ObjectsTable from "app/components/ObjectsTable";
import { Span } from "app/components/Typography";
import { BASE_BACKEND, BASE_OUTLET } from "app/utils/constant";
import ResponsiveDialog from "app/components/ResponsiveDialog";
import SimpleDialog from "app/components/SimpleDialog";
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

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

const fetchData = async(setContent) => {
  axios.get(BASE_BACKEND + BASE_OUTLET)
    .then((response) => {
      setContent(response.data)
    })
    .catch((error) => {
      console.error(error)
    })
}

function deleteOutlet(id, setTitle, setContent, setOpen){
  axios.delete(BASE_BACKEND + BASE_OUTLET, {data:{
    outlet_id: id
  }})
    .then((response) => {
      setTitle('Outlet deleted succesfully')
      setOpen(true)
    })
    .catch((error) => {
      setTitle('Error deleting outlet')
      setContent(error.message)
      setOpen(true)
    })
}

const AppOutletList = () => {

  const [refresh, setRefresh] = useState(0);
  const keyContent = ['id', 'name', 'path'];
  const headers = ['#', 'Name', 'Path'];
  const [content, setContent] = useState([]);
  const navigation = useNavigate();
  const [openDelete, setOpenDelete] = useState(false);
  const [openAlert, setOpenAlert] = useState(false);
  const [titleAlert, setTitleAlert] = useState('');
  const [contentAlert, setContentAlert] = useState('');
  const [active, setActive] = useState(-1);

  useEffect (() => {
      fetchData(setContent)
      setActive(-1)
  },[refresh])

  return (
    <Container>
      <Box className="breadcrumb">
        <Breadcrumb routeSegments={[{ name: "Outlets", path: "/outlets" }]} />
      </Box>

      <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'flex-end'}}>
        <StyledButton variant="contained" color="success" onClick={()=>{navigation('/outlets/create')}}>
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
          editButton={false}
          editAction={(index)=>{navigation('/outlet/edit/'+content[index].id)}}
          deleteButton={true}
          deleteAction={(index)=>{setOpenDelete(true); setActive(index)}}
        />
      </SimpleCard>
      <ResponsiveDialog
        open={openDelete}
        setOpen={setOpenDelete}
        title={active == -1 ? ('') : ('Delete outlet ' + content[active].name + '?')}
        contentText={'Are you sure you want to delete this outlet? This will break associated flows'}
        acceptAction={()=>{deleteOutlet(content[active].id, setTitleAlert, setContentAlert, setOpenAlert); setOpenDelete(false)}}
      />
      <SimpleDialog 
        open={openAlert}
        setOpen={setOpenAlert}
        title={titleAlert}
        contentText={contentAlert}
        handleClose={()=>{setOpenAlert(false);setRefresh(refresh+1)}}
      />
    </Container>
  );
};

export default AppOutletList;