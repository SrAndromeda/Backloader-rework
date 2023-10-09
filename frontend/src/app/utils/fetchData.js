import axios from "axios";
import { BASE_BACKEND_PROTOCOL, BASE_FLOW, BASE_OUTLET } from "app/utils/constant";

export const fetchFlow = async (setContent) => {
    axios.get(BASE_BACKEND_PROTOCOL + window.location.hostname + ':' + window.location.port + BASE_FLOW)
        .then((response) => {
            setContent(response.data)
            // console.log(response.data)
        })
        .catch((error) => {
            console.error(error)
        })
};

export const fetchOutlet = async (setContent) => {
    axios.get(BASE_BACKEND_PROTOCOL + window.location.hostname + ':' + window.location.port + BASE_OUTLET)
        .then((response) => {
            setContent(response.data)
            // console.log(response.data)
        })
        .catch((error) => {
            console.error(error)
        })
};