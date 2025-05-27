/* eslint-disable dot-notation */

import { Button, CopyButton } from "@mantine/core";
import { FaClipboard } from "react-icons/fa";
import { NavLink } from "react-router-dom";
import classes from "./EntityProfileComponents.module.css";
import { FkLinkReadParams } from "./MnfpEntityProfile";

interface DefaultReadComponentProps {
    propertyKey: string,
    title: string, 
    value: string
}

interface FkLinkReadComponentProps {
    propertyKey: string,
    title: string, 
    value: string
    displayValue: string,
    params: FkLinkReadParams
}

export const DefaultReadComponent: React.FC<DefaultReadComponentProps> = ({     
    propertyKey,
    title,
    value
}) => { 
  return (
    <div className={classes.entityProfileFieldBox} id={propertyKey}>
        <div className={classes.entityProfileFieldBoxPropertyTitleSection}>
        {title}:
        </div>
        <div className={classes.entityProfileFieldBoxPropertyValueSection}>
        <label>{value}</label>
        </div>
    </div>
  );  
} 

export const FkLinkReadComponent: React.FC<FkLinkReadComponentProps> = ({     
    propertyKey,
    title,
    value,
    displayValue,
    params
}) => { 
  return (
      <div className={classes.entityProfileFieldBox} id={propertyKey}>
        <div className={classes.entityProfileFieldBoxPropertyTitleSection}>
            {title}:
        </div>
        <div className={classes.entityProfileFieldBoxPropertyValueSection}> 
            {
            value 
            ? 
            <span>
                <NavLink 
                    to={`${params.profileUrl}/${value}`}
                >
                    {displayValue}
                </NavLink>    
                { 
                    value &&
                    <CopyButton value={value}>
                    {({ copied, copy }) => (
                        <Button 
                        style={{ marginLeft: 5 }}   
                        size='compact-xs' 
                        color={copied ? 'teal' : 'blue'} 
                        onClick={copy}
                        variant="subtle"
                        title="Copy id"
                        >
                        {copied ? <FaClipboard/> : <FaClipboard/>}
                        </Button>
                    )}
                    </CopyButton> 
                }
            </span>
            :
            <span>
                <label>------------</label>
            </span>
            }
        </div>
    </div>
  );  
} 