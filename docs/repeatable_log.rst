.. _repeatable_log:

=========================
Repeatable pydov sessions
=========================

Pydov can be used to integrate DOV data in your own scripts and analysis. By 
default it will execute a new search operation on every run, making it easy to
rerun your analysis at a later time using the latest data that might not have been
available before. This means your script and analysis will be reproducible.

For some projects or use-cases one might want to go a step further and want
full repeatability: when rerunning the script or analysis exactly the same 
results should be returned. Pydov supports this too, by allowing users to
save (record) a pydov session into an archive and replaying it afterwards.

This could for instance be used to record a session in the initial stage of your
research, and replay it from then on to always work with exactly the same dataset.
You can make modifications to the analysis parts of your script, as long as the
pydov calls remain the same it will be possible to replay the saved archive. The
advantage of this approach over another way or form of saving the pydov dataframes
is that the code to request the data remains in your script, and it also enables
rerunning the entire analysis with updated data simply by removing the replay hook.

It can also be used at the end of your research, to save a repeatable copy of your
analysis to disk for archiving purposes. This way, you can be sure it is reproducible
and repeatable, no matter what happens to the data in DOV.

Lastly, it could be used to share a session between collegues, students or tutors/mentors.
It enables them to rerun your session exactly as you saw it, while also allowing them
to both inspect the code and make changes to the analysis part.


Recording a pydov session
*************************

To record a pydov session, you can add the following to the top of your script.
It will add an instance of the RepeatableLogRecorder to the pydov hooks, which 
takes a single argument with the directory where the archive will be saved.

   ::

        import pydov
        from pydov.util.hooks import RepeatableLogRecorder

        pydov.hooks.append(
            RepeatableLogRecorder('.')
        )

When running your script, pydov will now create a new zip archive in the 
provided directory and save the entire session inside, including all metadata 
and search query responses, XML data and even pydov itself.

The archive will also contain a metadata.json file with some more details,
including the versions of key dependencies that were installed at the time of
recording. Also the timestamp of the recording is added:

    ::

        {
            "versions": {
                "pydov": "2.2.0",
                "owslib": "0.25.0",
                "pandas": "1.5.0rc0",
                "numpy": "1.23.1",
                "requests": "2.28.1",
                "fiona": "1.8.21",
                "geopandas": "0.11.1"
            },
            "timings": {
                "start": "20221006T152244",
                "end": "20221006T152246",
                "run_time_secs": 2.0412390239944216
            }
        }

After the script is finished, it will print the location of the archive 
containing the saved session.


Replaying a saved pydov session
*******************************

To replay a recorded session, you can add the following to the top of your 
script. It will prepend the saved session to your Python path, which makes sure
the next import(s) of pydov will import from the recorded archive. Next it
installs the RepeatableLogReplayer hook, which takes a single argument with the
location of the archive.

    ::

        import sys
        sys.path.insert(0, './pydov-archive-20221006T150643-997a6d.zip')

        import pydov
        from pydov.util.hooks import RepeatableLogReplayer

        pydov.hooks.append(
            RepeatableLogReplayer('./pydov-archive-20221006T150643-997a6d.zip')
        )

Distribute this modified version of your script together with the pydov archive,
executing it will now always yield the same results.

Note: in order to have full reproducible runs it is advised to also install the
same versions of pydov's dependencies as were used when recording. These version
numbers can be found in the metadata.json file inside the archive.